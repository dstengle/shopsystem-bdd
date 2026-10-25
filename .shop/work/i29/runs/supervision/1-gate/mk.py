import json
L = {
 "r105": "[r105] When `work run` finds an initiative that is not `done`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.",
 "r106": "[r106] When `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch.",
 "r107": "[r107] If a change list that `work run` reads names a capability that `spec/capabilities/` does not have, then `work run` shall write no capability-proposal for it and exit with an error, naming the capability.",
}
q = [
 "supervision r105, the term 'every raised request'. Line (added): " + L["r105"] + " Readings: (a) keep the wording, as work-queue r23 words it [recommended]; (b) 'every request that a round of the initiative raised'.",
 "supervision r105, an initiative with no work-item. Line (added): " + L["r105"] + " As drafted it also fires for an initiative with none. Readings: (a) add 'that has at least one work-item' [recommended]; (b) as drafted.",
 "supervision r105 against r106 and the measure/analysis rounds, order. Line (added): " + L["r105"] + " An initiative set `done` first may never be measured or analysed (r66 skips `done`). Readings: (a) r105 adds 'and whose measurement and analysis record `work run` has committed' [recommended]; (b) as drafted.",
 "Commit of the `done` status (new line or none). Concerns r105 and " + L["r106"] + " Readings: (a) add a line: 'When `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch.' [recommended]; (b) add nothing.",
 "supervision r107, a capability the round adds. Line (added): " + L["r107"] + " Readings: (a) exempt it: '...neither `spec/capabilities/` nor the round's drafts have...' [recommended]; (b) refuse it too, as drafted.",
 "supervision r107 and r92, what is written when one capability is missing. Line (added): " + L["r107"] + " Readings: (a) only the missing capability gets no proposal, r92 still writes the others, as drafted [recommended]; (b) none: '...shall write no capability-proposal for the change list and exit with an error, naming the capability.'",
]
json.dump({"status": "DONE", "summary": "Gate of supervision: 6 questions on r105, r107 and r106 (r108 raised none).", "questions": q}, open(".shop/scratch/1-gate/result.json", "w"))
