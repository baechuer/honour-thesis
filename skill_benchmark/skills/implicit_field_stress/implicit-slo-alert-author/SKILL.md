---
name: implicit-slo-alert-author
description: "Produces alerting rules from SLOs, metric names, windows, labels, and severity policy."
---

# Implicit Slo Alert Author

This routine translates reliability goals into alerts. It needs metric names, thresholds, windows, and severity labels. The output is an alert rule and verification query. If the user wants a dashboard, an incident narrative, or trace diagnosis, choose a different routine.
