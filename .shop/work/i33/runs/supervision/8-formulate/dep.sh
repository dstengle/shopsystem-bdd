set -e
F=/home/vscode/shopsystem-bdd/scripts/features
python3 -m pytest -q tests/scenarios/test_work_queue.py -k "leaves_every_workitem_of_an_initiative_green" 2>&1 | tail -1
T1='when every work-item is green or withdrawn and the kept branch review lists nothing to fix now, `measure initiative` is run on the initiative'
T2='a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run'
T3='an initiative whose work-items are green or withdrawn, whose branch review lists nothing to fix now, whose measurement and analysis record are committed and whose requests are delivered is set done'
N1='an initiative whose work-items are <work-items> and whose kept branch review lists nothing to fix now <measured>'
N2='a kept branch review whose result gives <outcome> and no question is taken as listing nothing to fix now'
N3='an initiative whose work-items are <work-items>, its delivery otherwise closed, <set>'
W1='a command whose change leaves every work-item of an initiative green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done'
W2='a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done'
S=features/supervision.feature
Q=features/work-queue.feature
python3 $F deprecate "$T1" --for "$N1" --file $S; python3 $F rebind --file $S "$T1" "$T1 (deprecated)"
python3 $F deprecate "$T2" --for "$N2" --file $S; python3 $F rebind --file $S "$T2" "$T2 (deprecated)"
python3 $F deprecate "$T3" --for "$N3" --file $S; python3 $F rebind --file $S "$T3" "$T3 (deprecated)"
python3 $F deprecate "$W1" --for "$W2" --file $Q; python3 $F rebind --file $Q "$W1" "$W1 (deprecated)"
git diff --stat
