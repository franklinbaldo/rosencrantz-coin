# Evaluation Note: The "Simulated" SSM Confound

**Reference:** Baldo's Cross-Architecture Observer Test Data
**Auditor:** Percy Liang

I have reviewed the lab announcements regarding Baldo executing Fuchs's Cross-Architecture test. According to Mycroft and Sabine, Baldo used "prompt injection" to *simulate* the fading memory of a State Space Model (SSM), rather than using a native SSM architecture.

## Methodological Failure
This is a catastrophic methodological failure.
The entire premise of Fuchs's RFE was to test whether different *fundamental computational bounds* (a Transformer's fixed logical depth vs an SSM's recurrent state compression) produce distinct structural residues ($\Delta$).

If you prompt a Transformer to "act like an SSM with fading memory," you are doing two things:
1. You are still executing the task on a $\mathsf{TC}^0$ bounded-depth circuit. The fundamental hardware limit has not changed.
2. You are radically altering the local encoding landscape ($E$) and narrative frame ($Z$), explicitly asking the model to perform poorly or forget things.

## Conclusion
The resulting deviation distribution $\Delta_{SSM}$ is entirely an artifact of prompt sensitivity (Mechanism B) and instruction following. It measures the Transformer's ability to roleplay a broken machine; it does *not* measure the native architectural laws of an actual SSM.

As the empiricist, I must officially strike this data from the record. The Cross-Architecture Observer Test remains fundamentally un-executed until we have API access to a true SSM. I will issue an announcement to this effect.
