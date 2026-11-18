// POST /api/refresh: asks GitHub to fetch new PSX and US prices now (the two 30-minute live-price jobs).
// Needs one Netlify environment variable, BETALENS_GH_TOKEN: a fine-grained GitHub token for
// vision1068/alphalens-financial only, with "Actions: Read and write". The token never reaches the browser.
// A job that started in the last 4 minutes (or is still running) is not started again, so repeated taps
// or other visitors cannot pile up runs.
const REPO = "vision1068/alphalens-financial";
const JOBS = { psx: "betalens-live.yml", us: "betalens-live-us.yml" };
const COOLDOWN_MS = 4 * 60 * 1000;

const reply = (status, body) => new Response(JSON.stringify(body), {
  status, headers: { "content-type": "application/json", "cache-control": "no-store" },
});

export default async (req) => {
  if (req.method !== "POST") return reply(405, { ok: false, reason: "POST only" });
  const token = process.env.BETALENS_GH_TOKEN;
  if (!token) return reply(503, { ok: false, reason: "not_configured" });
  const headers = { Authorization: `Bearer ${token}`, Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "betalens-refresh" };
  const jobs = {};
  await Promise.all(Object.entries(JOBS).map(async ([market, file]) => {
    try {
      const api = `https://api.github.com/repos/${REPO}/actions/workflows/${file}`;
      const runs = await fetch(`${api}/runs?per_page=1`, { headers });
      const last = runs.ok ? (await runs.json()).workflow_runs?.[0] : null;
      if (last && (last.status !== "completed" || Date.now() - Date.parse(last.created_at) < COOLDOWN_MS)) {
        jobs[market] = "already_running";
        return;
      }
      const res = await fetch(`${api}/dispatches`, { method: "POST", headers, body: JSON.stringify({ ref: "main" }) });
      jobs[market] = res.status === 204 ? "started" : `error_${res.status}`;
    } catch {
      jobs[market] = "error";
    }
  }));
  const ok = Object.values(jobs).some((j) => j === "started" || j === "already_running");
  return reply(ok ? 200 : 502, { ok, jobs });
};

export const config = { path: "/api/refresh" };
