# Chapter 21: Exercises

Attempt the exercises first. Where an answer depends on policy, state the choice and its consequences.

### Exercises

1. **Freshness.** Replace equality with `draft_version <= current_version`. Give a state accepted by the revised rule but rejected by the original.
2. **Safety and progress.** A gate always returns `False`. Which property can it satisfy, and what might it fail?
3. **Unknown consent.** What should happen under R5, and what operational contract is additionally needed?
4. **Race and binding point.** Consent is checked at 10:00, withdrawn at 10:01 and the governed send occurs at 10:02. Does the first model’s safety property hold?
5. **Retry.** A request commits while consent is valid. Consent is withdrawn. An identical retry returns `duplicate`. Is that necessarily a new violation?
6. **Audit oracle.** Propose two tests beyond `contains_summary`. State a remaining limitation.
7. **Bypass.** A worker has a second credential that writes directly to the delivery queue. What happens to the proof?
8. **Consent scope.** Preparation is authorised, but disclosure to the selected recipient is not. What is wrong with global `valid`?
9. **Distributed boundary.** Consent storage and the provider cannot participate in one transaction. Give two designs and their limitations.
10. **Assurance argument.** State one claim, two supporting evidence items and one defeater for the hypothetical authority.
