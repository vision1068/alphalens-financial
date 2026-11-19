// The BetaLens timetable, run by Netlify every 30 minutes (GitHub's own schedule proved unreliable:
// runs hours late or not at all). Times are UTC.
//   PSX prices:   Mon-Fri 04:00-11:59 (09:00-16:59 Pakistan time)
//   US prices:    Mon-Fri 13:00-23:59 and Tue-Sat 00:00-00:59 (US pre-market, trading and after-hours)
//   Daily scores, AI notes and alerts: every day at the 04:37 tick (09:37 Pakistan time)
import { JOBS, startJob, token } from "../lib/github.mjs";

export function dueJobs(now) {
  const day = now.getUTCDay();          // 0 Sunday … 6 Saturday
  const hour = now.getUTCHours();
  const weekday = day >= 1 && day <= 5;
  const due = [];
  if (weekday && hour >= 4 && hour <= 11) due.push("psx");
  if ((weekday && hour >= 13) || (day >= 2 && day <= 6 && hour === 0)) due.push("us");
  if (hour === 4 && now.getUTCMinutes() >= 30) due.push("daily");
  return due;
}

export default async () => {
  if (!token()) {
    console.log("BETALENS_GH_TOKEN is not set; nothing started");
    return;
  }
  for (const job of dueJobs(new Date())) {
    const result = job === "daily"
      ? await startJob(JOBS.daily, { cooldownMs: 60 * 60 * 1000, inputs: { daily_analysis: "true" } })
      : await startJob(JOBS[job], { cooldownMs: 20 * 60 * 1000 });
    console.log(`${job}: ${result}`);
  }
};

export const config = { schedule: "7,37 * * * *" };
