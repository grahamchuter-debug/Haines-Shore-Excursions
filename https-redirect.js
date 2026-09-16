const ORIGIN = "https://hainesshoreexcursions.com";

const STATIC_EXT =
  /\.(css|js|mjs|map|png|jpe?g|gif|webp|svg|ico|txt|xml|json|jsonc|woff2?|ttf|eot|pdf|webmanifest|md|sh|py|ts|tsx|toml)$/i;

const BLOCK_PREFIXES = [
  "/.git",
  "/content",
  "/partials",
  "/scripts",
  "/node_modules",
  "/.wrangler",
  "/package.json",
  "/package-lock.json",
  "/wrangler.jsonc",
  "/wrangler.toml",
  "/https-redirect.js",
  "/deploy.sh",
  "/js/site.js",
];

const KNOWN_PAGES = new Set([
  "",
  "best-haines-shore-excursions",
  "haines-cruise-port-guide",
  "things-to-do-in-haines-from-a-cruise-ship",
  "haines-wildlife-guide",
  "haines-bald-eagle-guide",
  "haines-vs-skagway",
  "chilkoot-lake-guide",
  "chilkat-bald-eagle-preserve-guide",
  "best-time-to-visit-haines",
  "haines-cruise-ship-schedule",
  "haines-cruise-planner",
  "haines-faq",
  "enquire",
  "bald-eagle-viewing-tours",
  "chilkoot-lake-wildlife-tour",
  "chilkoot-river-tour",
  "scenic-haines-tour",
  "fort-seward-tour",
  "photography-tours",
  "cultural-heritage-tours",
  "nature-walks",
]);

function isBlocked(pathname) {
  const lower = pathname.toLowerCase();
  return BLOCK_PREFIXES.some(
    (p) => lower === p || lower.startsWith(`${p}/`) || lower.startsWith(p),
  );
}

function isStaticAsset(pathname) {
  return STATIC_EXT.test(pathname);
}

function pageKey(pathname) {
  let p = pathname || "/";
  try {
    p = decodeURIComponent(p);
  } catch {
    /* keep */
  }
  if (p.toLowerCase().endsWith(".html")) p = p.slice(0, -5);
  p = p.replace(/\/+$/, "");
  if (p.startsWith("/")) p = p.slice(1);
  return p;
}

function toCanonical(pathname, search) {
  let path = pathname || "/";
  try {
    path = decodeURIComponent(path);
  } catch {
    /* keep */
  }
  if (path.toLowerCase().endsWith(".html")) path = path.slice(0, -5);
  if (path !== "/" && !path.endsWith("/")) path = `${path}/`;
  return `${ORIGIN}${path}${search || ""}`;
}

async function notFound(env, request) {
  // Trigger Workers Assets not_found_handling (404.html) without copying redirect headers
  const assetRes = await env.ASSETS.fetch(
    new Request(`${ORIGIN}/__haines_missing_path__/`, request),
  );
  const headers = new Headers(assetRes.headers);
  headers.delete("Location");
  headers.set("Cache-Control", "no-store");
  return new Response(assetRes.body, {
    status: 404,
    statusText: "Not Found",
    headers,
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (isBlocked(url.pathname)) {
      return notFound(env, request);
    }

    const key = pageKey(url.pathname);
    const isHtmlExt = url.pathname.toLowerCase().endsWith(".html");
    const needsSlash =
      !isStaticAsset(url.pathname) &&
      url.pathname !== "/" &&
      (!url.pathname.endsWith("/") || isHtmlExt);

    // HTTP → HTTPS (and slash canonical when known page)
    if (url.protocol === "http:") {
      if (KNOWN_PAGES.has(key)) {
        return Response.redirect(toCanonical(url.pathname, url.search), 301);
      }
      if (needsSlash && !KNOWN_PAGES.has(key) && !isStaticAsset(url.pathname)) {
        // Unknown path: single hop to https URL, then 404 without soft homepage
        return Response.redirect(`${ORIGIN}${url.pathname}${url.search}`, 301);
      }
      return Response.redirect(`${ORIGIN}${url.pathname}${url.search}`, 301);
    }

    // Known page bare/.html → trailing-slash 301
    if (needsSlash && KNOWN_PAGES.has(key)) {
      return Response.redirect(toCanonical(url.pathname, url.search), 301);
    }

    // Unknown bare path → branded 404 (no slash soft-404 dance)
    if (needsSlash && !isStaticAsset(url.pathname)) {
      return notFound(env, request);
    }

    return env.ASSETS.fetch(request);
  },
};
