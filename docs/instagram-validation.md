# Instagram: safe validation

Validate without images, filesystem writes, git, credentials or API calls:

```sh
python scripts/ig_auto_post.py --dry-run
python -m unittest discover -s tests -p 'test_ig_safe_validation.py' -v
```

The complete queue is validated before any effects. Three-field slides are preserved; for four-field slides the extra note is rendered as a new paragraph in the small-text area. Empty fields, duplicate topic IDs, and unsupported slide counts are rejected.

Normal publishing now requires IG_ACCESS_TOKEN, IG_USER_ID and GITHUB_REPOSITORY before generating or committing files. Do not put these values in documents or tests. Publication is cancelled if carousel processing reports ERROR/EXPIRED or never reaches FINISHED.

Local regression: 12 tests passed; dry-run validated 12 topics and 24 slides. Financial facts in the existing queue were not independently verified by this code fix. Review content and credentials before authorizing a merge that reactivates scheduled publication. No public publisher was executed to test this PR.
