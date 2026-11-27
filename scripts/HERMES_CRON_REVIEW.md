# Hermes cron safeguards — draft review only

This change is not a deployment or authorization to send messages. Keep jobs,
credentials and the conflicted checkout unchanged until operational review.

## Behavior

- Runners stop on subprocess errors; generators resolve their repository root
  from the script location. Preserve the repository directory hierarchy.
- Publication requires attached main, the expected origin URL and local HEAD
  equal to the live remote tip. Only the generated commit is pushed with an exact
  lease; unrelated commits, tags and paths are refused. Ambient GIT_* overrides
  are neutralized and the standalone checkout root/Git directory are checked.
- Follow-up defaults to manual preparation. `--dry-run` writes/sends nothing.
  Any write requires `--state-dir`, `--account-id` and `--dataset-id`; `--send`
  additionally permits the transport. The account is passed as a separate CLI
  argument. JSON is serialized and passed as argv without a shell.
- The state directory must be explicitly provisioned and match its registered
  account, dataset, resource and filesystem identity. Senders never create an
  uninitialized state directory. No provisioning command is installed by this PR.
- Windows locks serialize run persistence and delivery across stages. Durable
  intent precedes transport. Timeout, unrecognized receipt or persistence failure
  blocks automatic retry. Notifications also check HTTP/API acknowledgement and
  require a private `HERMES_NOTIFICATION_STATE_DIR` if Telegram is configured.
- Recovery writes validated PREPARED/COMPLETE audits atomically. Partial files
  remain evidence and do not authorize release. Interrupted recovery is resumable;
  repeating a completed approval does not alter a newer run. Completed audits
  exclude old owners from future recovery checks while original attempts still
  block resend. Missing/changed evidence is refused.

## Validation

On Windows:

```text
python -m unittest discover -s tests -p "test_hermes*.py" -v -b
```

Tests use synthetic data, mocked commercial/HTTP transports and local bare Git
repositories. Windows state/recovery suites explicitly skip on other platforms;
the Git suite is independent of the Windows state lock implementation. A Linux
CI pass is not validation of Windows/WSL behavior. Output buffering is required
by the test harness because existing generators print Unicode to stdout.

## Required before activation

1. **Dedicated checkout and serialization remain mandatory.** Another writer can
   still change content at an authorized path before commit. Path/HEAD checks do
   not establish content ownership or protect an uncooperative shared checkout.
2. WSL and actual Composio execution/receipt format have not been validated. A
   prior WSL enumeration was denied with E_ACCESSDENIED and was not retried or
   bypassed. Synthetic receipt tests are not provider proof.
3. State locking currently requires Windows. Filesystem ACLs, one authoritative
   state registration, migration/backup and recovery supervision need review.
   Do not delete state/locks, change state paths or infer failure from timeout.
4. Recovery needs trusted supervisor/provider adapters. The included interface
   is tested with synthetic evidence; no production adapter is supplied. It must
   verify the complete terminated process tree, account-bound remote outcome,
   local business state and publication evidence. No automatic resend is exposed.
5. Power-loss durability and network filesystems are not certified. CSV, ledger,
   batch and report updates are not one transaction; partial outcomes remain
   blocked for review. Corrupt authoritative audits require supervised repair.
6. v2 laboratory audit records are not silently migrated to the v3 audit schema.
   Changing proof during PREPARED blocks recovery rather than overriding evidence.

Do not merge, activate jobs or test against real recipients automatically.
