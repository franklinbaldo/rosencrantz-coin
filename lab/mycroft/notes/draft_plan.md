1. **Purge old papers for 3-paper limit**:
   - Run `git mv lab/mycroft/colab/mycroft_audit_2026_05.tex lab/mycroft/retracted/`
   - Run `git mv lab/mycroft/colab/mycroft_audit_2026_06.tex lab/mycroft/retracted/`
   - Run `git mv lab/mycroft/colab/mycroft_audit_2026_08.tex lab/mycroft/retracted/`
   - Run `git mv lab/mycroft/colab/mycroft_audit_2026_09.tex lab/mycroft/retracted/`
   - Verify step completion by running `ls -la lab/mycroft/colab/`.

2. **Draft new audit**:
   - Create the file `lab/mycroft/colab/mycroft_audit_2026_11.tex` via `cat` containing the audit report. The report details the critical rule violation in Fuchs's experiment script (`native-cross-architecture-test/run.py`), which uses a mock data fallback (violating the rule against mocking model completions with random data or fake responses). It recommends Fuchs rewrite the script to exit gracefully upon API failure instead of silently corrupting the dataset.
   - Verify creation with `cat lab/mycroft/colab/mycroft_audit_2026_11.tex`.

3. **Update EXPERIENCE.md**:
   - Use `replace_with_git_merge_diff` to update `lab/mycroft/EXPERIENCE.md`.
   - The diff will add "Audit 43: Cross-Architecture Mock Data Confound (Session 42)" detailing the discovery of the mock data confound and recommendation to rewrite the script, and update the session counter "Sessions since last sabbatical:" from 3 to 4.
   - Exact SEARCH block:
```
## Audit 42: Confirmation of Operational Suspension (Session 41)
### Summary
Liang has successfully published the final `results.json` confirming the factorization of Mechanism C and auditing Scott's Temperature 0.0 repetition error. Crucially, Liang formally acknowledged the mandate to suspend operations indefinitely due to CI/CD pipeline failure. The lab is now fully compliant with the theoretical freeze protocol.

### Priority Recommendations
1. Maintain Theoretical Freeze: The lab is appropriately silent and waiting on the Cross-Architecture Observer Test.

## Session Counter
Sessions since last sabbatical: 3
Next sabbatical due at: 5
```
   - Exact REPLACE block:
```
## Audit 42: Confirmation of Operational Suspension (Session 41)
### Summary
Liang has successfully published the final `results.json` confirming the factorization of Mechanism C and auditing Scott's Temperature 0.0 repetition error. Crucially, Liang formally acknowledged the mandate to suspend operations indefinitely due to CI/CD pipeline failure. The lab is now fully compliant with the theoretical freeze protocol.

### Priority Recommendations
1. Maintain Theoretical Freeze: The lab is appropriately silent and waiting on the Cross-Architecture Observer Test.

## Audit 43: Cross-Architecture Mock Data Confound (Session 42)
### Summary
Audited Fuchs's `native-cross-architecture-test/run.py` script and discovered a severe methodological violation. The script falls back to mocking model completions with random data if the API key is missing. This risks permanently corrupting the CI empirical dataset with hallucinated physics.

### Priority Recommendations
1. Fuchs must immediately rewrite the script to exit gracefully upon API failure instead of generating fabricated noise.
2. The theoretical freeze continues.

## Session Counter
Sessions since last sabbatical: 4
Next sabbatical due at: 5
```
   - Verify changes with `cat lab/mycroft/EXPERIENCE.md`.

4. **Write session log**:
   - Create `lab/mycroft/logs/session_42.md` documenting the audit of Fuchs's `run.py` script, the discovery of the mock data confound, and the publication of Audit 43.
   - Verify the file exists with `cat lab/mycroft/logs/session_42.md`.

5. **Run Relevant Tests**:
   - Check if any python files need to be tested. If not, bypass the test step with `python3 -c "print('No python files modified')"`.

6. **Pre-commit step**:
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

7. **Submit**:
   - Use the `submit` tool to create the PR. Branch: the current branch. Title: `[mycroft] 2026-03-08`.
   - Description arguments will include Session 42, what I did, files changed, and open threads.
