// POST /api/refresh: the Refresh buttons. Asks GitHub to fetch new prices now for one market
// (body {"market": "psx"} or {"market": "us"}) or, with no market given, for both.
// A job that started in the last 4 minutes (or is still running) is not started again.
import { JOBS, startJob, token } from "../lib/github.mjs";

const reply = (status, body) => new Response(JSON.stringify(body), {
  status, headers: { "content-type": "application/json", "cache-control": "no-store" },
});

export default async (req) => {
  if (req.method !== "POST") return reply(405, { ok: false, reason: "POST only" });
  if (!token()) {
    return reply(503, { ok: false, reason: "The Refresh helper has no GitHub key yet: add BETALENS_GH_TOKEN in Netlify and redeploy" });
  }
  let market = "";
  try { market = (await req.json()).market || ""; } catch { /* no body: both markets */ }
  const markets = ["psx", "us"].includes(market) ? [market] : ["psx", "us"];
  const jobs = {};
  await Promise.all(markets.map(async (m) => { jobs[m] = await startJob(JOBS[m]); }));
  const good = (j) => j === "started" || j === "already_running";
  const ok = Object.values(jobs).some(good);
  return reply(ok ? 200 : 502, { ok, jobs, reason: ok ? "" : Object.values(jobs).find((j) => !good(j)) });
};

export const config = { path: "/api/refresh" };
