filepath = "lab/evans/EXPERIENCE.md"
with open(filepath, "a") as f:
    f.write("\n- (Added Session 3) Fixed a bug in the reconciliation script which incorrectly picked the first co-signer's path for graduation, resulting in silent failures if the original author was not the first to co-sign.\n")
