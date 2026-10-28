"""`work run`'s branch review (capability supervision): when it is due, the `bdd-branch-reviewer` session over the
initiative branch, and the keeping of its directory in the initiative. Standard library only; a part of supervise.Run."""
import shutil
import uuid

from supervise_worker import SCRIPTS, git, with_transcript
from workqueue import Refused

AGENT = "bdd-branch-reviewer"
STAGE = "branch-review"


class Reviews:
    """The part of supervise.Run that reviews the initiative branch once its work-items are done."""

    def review_dir(self):
        return self.dir / "runs" / STAGE

    def unread(self):
        """The commits on the initiative branch from its base that no kept branch review has read (r27, r50): not
        reachable from the `Head:` of any kept review's brief, and not a kept review's own commit, which holds only its
        directory and log.jsonl."""
        heads = []
        for brief in sorted(self.review_dir().glob("*/brief.md")):
            heads += [line.split(":", 1)[1].strip() for line in brief.read_text().splitlines() if line.startswith("Head:")]
        base = self.base()
        shas = git(self.root, "rev-list", "HEAD", *["^" + r for r in ([base] if base else []) + heads]).stdout.split()
        kept = self.rel(self.review_dir()) + "/"
        log = self.rel(self.dir / "log.jsonl")
        def own(sha):     # a merge commit's diff-tree is empty: it is no review's own commit
            paths = git(self.root, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", sha).stdout.split()
            return bool(paths) and all(p.startswith(kept) or p == log for p in paths)
        return [sha for sha in shas if not own(sha)]

    def unread_mine(self):
        """The unread commits (r27, r50) that touch this initiative's own files, its log and kept reviews aside: on a
        branch the initiatives share, another initiative's commits call for no review of this one (each work-item's
        transition commits a file of the initiative, so its new work does)."""
        mine = self.rel(self.dir) + "/"
        kept = self.rel(self.review_dir()) + "/"
        log = self.rel(self.dir / "log.jsonl")
        def touches(sha):
            paths = git(self.root, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", "-m", sha).stdout.split()
            return any(p.startswith(mine) and not p.startswith(kept) and p != log for p in paths)
        return [sha for sha in self.unread() if touches(sha)]

    def branch_review(self):
        """A `bdd-branch-reviewer` session over the initiative branch from its base, in a detached worktree of its own,
        given one brief (r27); the push of the branch verified first (r35, r51). Its directory is kept and committed
        when its session ends (r47, r48). The kept directory; None when no review was due."""
        if not self.unread_mine():
            return None
        reason = self.git_push("--dry-run")
        if reason:
            raise Refused("work run could not verify that it can push the initiative branch %s before the branch "
                          "review: it cannot push the initiative branch to the remote %s: %s"
                          % (self.branch, self.remote(), reason))
        self.log(stage=STAGE, event="push verified")
        k = len([p for p in self.review_dir().iterdir() if p.is_dir()]) + 1 if self.review_dir().is_dir() else 1
        tree = self.worktree(None, STAGE)
        here = tree / ".shop" / "scratch" / STAGE
        here.mkdir(parents=True)
        path = here / "brief.md"
        path.write_text("# branch review of %s\n\nInitiative: %s\nAgent: %s\nScripts: %s\n"
                        "Initiative branch: %s\nBase: %s\nHead: %s\nWorktree: %s\nRun directory: %s\nResult file: %s\n\n"
                        "Review the initiative branch from its base. You start in your worktree: run every command "
                        "from there and never change directory. Write the result file first, with the outcome "
                        "`PARTIAL`, and keep it current as you work: JSON with `status`, `summary` and "
                        "`questions`.\n"
                        % (self.initiative, self.rel(self.dir), AGENT, SCRIPTS, self.branch, self.base(),
                           git(self.root, "rev-parse", "HEAD").stdout.strip(), tree, here, here / "result.json"))
        session = str(uuid.uuid4())
        self.log(stage=STAGE, agent=AGENT, session=session, event="start")
        try:
            with self.slots:     # one of the sessions the limit allows, with those of every initiative taken (r60)
                done = self.session(STAGE, AGENT, path, session, tree, None)
            kept = self.review_dir() / str(k)
            with self.lock:     # the checkout's files are written and committed at once: another initiative's run sees them
                shutil.copytree(here, kept)
                self.own.add(self.rel(kept))
                (kept / "session.json").write_text(with_transcript(done.stdout, session))
                self.log(stage=STAGE, agent=AGENT, session=session, event="end")
                rels = [self.rel(kept), self.rel(self.dir / "log.jsonl")]
                git(self.root, "add", "--", *rels)
                git(self.root, "commit", "-q", "-m", "branch review %d of %s" % (k, self.initiative), "--", *rels)
                self.unlogged = []
                self.own.discard(self.rel(kept))
        finally:
            self.remove(tree)
        reason = self.git_push()
        if reason:      # the review stays committed locally; the next run pushes it first (r54)
            raise Refused("the branch review is committed, but it cannot push the initiative branch to the "
                          "remote %s: %s" % (self.remote(), reason))
        return kept
