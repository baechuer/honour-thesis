billing -> account: customer lookup
billing -> notification: invoice email
notification -> analytics: event emit
analytics -> billing_db: nightly read
