p='spec/capabilities/supervision.md'
s=open(p).read()
def after(key,new):
    global s
    i=s.index(key); j=s.index('\n',i)+1
    s=s[:j]+new+'\n'+s[j:]
def rep(a,b):
    global s
    assert s.count(a)==1; s=s.replace(a,b)
after('- [r66]','- [r111] **When** a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends.')
rep('**When** every question of a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers.','**When** every question that a round of the kind `gate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `apply` given the answers.')
after('- [r70]','- [r116] **When** every question that a round of the kind `formulate` gave on a capability-proposal has an answer, `work run` shall start a round of the kind `formulate` for the proposal, given the answers.')
after('- [r80]','- [r114] **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal\'s `adds`, `changes` and `removes` from the change list the round applied.')
rep('started for a capability-proposal ends, `work run` shall transition the proposal to `formulated`.','started for a capability-proposal ends without giving a question, `work run` shall transition the proposal to `formulated`.')
after('- [r83]','- [r112] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives questions, `work run` shall write each question its result gives under the proposal\'s `## Questions`.\n- [r113] **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall transition the proposal to `awaiting-answer`.')
after('- [r88]','- [r115] **If** a round of any kind that `work run` started for a capability-proposal or an initiative gives an outcome other than `DONE`, ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall take the initiative\'s other nodes through their transitions before it exits with an error.')
open(p,'w').write(s)
