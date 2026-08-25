SELECT service,
       COUNT(*) AS incidents,
       ROUND(AVG(resolution_hours)::numeric, 2) AS avg_mttr_hours,
       ROUND(SUM(downtime_hours)::numeric, 2) AS downtime_hours,
       ROUND(100.0 * AVG(CASE WHEN resolution_hours > sla_hours THEN 1 ELSE 0 END)::numeric, 2)
           AS sla_breach_pct
FROM incidents
GROUP BY service
ORDER BY sla_breach_pct DESC, incidents DESC;

SELECT DATE_TRUNC('month', opened_at) AS month,
       COUNT(*) AS incidents,
       ROUND(SUM(downtime_hours)::numeric, 2) AS downtime_hours
FROM incidents
GROUP BY 1
ORDER BY 1;
