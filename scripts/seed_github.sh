#!/usr/bin/env bash
# Recreate todo-api's open issues and the draft PR #12 in your GitHub copy.
# Needs: gh (logged in), run from the repository root, branch feature/tags pushed.
set -euo pipefail

repo=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Seeding issues in $repo"

count=$(gh issue list --state all --limit 1 --json number -q 'length')
pulls=$(gh pr list --state all --limit 1 --json number -q 'length')
if [ "$count" = "0" ] && [ "$pulls" = "0" ]; then
  # Empty tracker: fill numbers 1-5 with closed placeholders so the open issues
  # get the same numbers as in docs/history/README.md (#6 to #11, draft PR #12).
  for t in "Initial release (v0.1.0)" "Search tasks by title" \
           "PR #3: search tasks by title (merged 2026-09-03, see docs/history)" \
           "Paginate GET /tasks" \
           "PR #5: pagination (merged 2026-10-01, see docs/history)"; do
    n=$(gh issue create --title "$t" --body "History record. See docs/history/README.md." | grep -o '[0-9]*$')
    gh issue close "$n" >/dev/null
  done
else
  echo "Note: this repo already has issues or PRs, so the numbers will not match #6 to #12."
fi

issue() { gh issue create --title "$1" --body "$2" >/dev/null && echo "  created: $1"; }

issue "GET /tasks/{id} and PATCH /tasks/{id} return 500 for an unknown id" \
  "GET /tasks/9999 and PATCH /tasks/9999 answer 500 Internal Server Error. They should answer 404."
issue "Empty and very long titles are accepted" \
  'POST /tasks with "title": "" or a 500-character title creates a task. MAX_TITLE in src/todo/services/tasks.py is never checked.'
issue "?page=1 skips the first page of tasks" \
  "With 3 tasks, GET /tasks?page=1&size=2 returns only the third task. Page 1 should be the first two."
issue "Optional due dates and an overdue filter" \
  "Let users give a task an optional due date and list the tasks that are overdue."
issue "Delete a task" \
  "There is no way to delete a task."
issue "Tags on tasks" \
  "Let users label tasks (work, home, ...) and filter by tag. Work in progress on branch feature/tags."

gh pr create --draft --base main --head feature/tags \
  --title "Tags on tasks (WIP)" \
  --body "Work in progress for the tags issue. Not ready for review." >/dev/null
echo "  created: draft PR from feature/tags"
echo "Done."
