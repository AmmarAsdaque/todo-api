# Project history

Times are UTC. Issues and pull requests were tracked on GitHub; this file keeps
the record in the repository so it survives forks and template copies.

## Releases

| Tag | Released and deployed | What changed |
| --- | --- | --- |
| v0.1.0 | 2026-08-14 09:00 | Create, read, list and update tasks |
| v0.2.0 | 2026-09-04 10:00 | Search tasks by title (issue #2, PR #3) |
| v0.3.0 | 2026-10-02 09:30 | Pagination for GET /tasks (issue #4, PR #5) |

## Shipped changes

### Issue #2: Search tasks by title → PR #3 → v0.2.0

| Event | Time |
| --- | --- |
| Issue #2 opened | 2026-09-01 08:00 |
| First commit on `feature/search` | 2026-09-02 10:00 |
| PR #3 opened | 2026-09-02 16:00 |
| First review ("search should ignore case") | 2026-09-03 12:00 |
| PR #3 merged | 2026-09-03 18:00 |
| v0.2.0 deployed | 2026-09-04 10:00 |

### Issue #4: Paginate GET /tasks → PR #5 → v0.3.0

| Event | Time |
| --- | --- |
| Issue #4 opened | 2026-09-22 09:00 |
| First commit on `feature/pagination` | 2026-09-29 10:15 |
| PR #5 opened | 2026-09-30 17:00 |
| First review | 2026-10-01 10:30 |
| PR #5 merged | 2026-10-01 13:00 |
| v0.3.0 deployed | 2026-10-02 09:30 |

Check the git side yourself:

```bash
git log --merges --oneline
git log --reverse --date=iso --format="%ad  %s" <merge-hash>^1..<merge-hash>^2
git tag -n1 v0.2.0
```

## Open issues

| # | Title | Opened |
| --- | --- | --- |
| 6 | GET /tasks/{id} and PATCH /tasks/{id} return 500 for an unknown id | 2026-10-09 |
| 7 | Empty and very long titles are accepted | 2026-10-10 |
| 8 | `?page=1` skips the first page of tasks | 2026-10-12 |
| 9 | Optional due dates and an overdue filter | 2026-10-13 |
| 10 | Delete a task | 2026-10-14 |
| 11 | Tags on tasks | 2026-10-14 |

### #6 GET /tasks/{id} and PATCH /tasks/{id} return 500 for an unknown id

`GET /tasks/9999` and `PATCH /tasks/9999` answer 500 Internal Server Error.
They should answer 404.

### #7 Empty and very long titles are accepted

`POST /tasks` with `"title": ""` or a 500-character title creates a task.
`MAX_TITLE` in `src/todo/services/tasks.py` is never checked.

### #8 `?page=1` skips the first page of tasks

With 3 tasks, `GET /tasks?page=1&size=2` returns only the third task. Page 1
should be the first two.

### #9 Optional due dates and an overdue filter

Let users give a task an optional due date and list the tasks that are overdue.

### #10 Delete a task

There is no way to delete a task.

### #11 Tags on tasks

Let users label tasks (`work`, `home`, ...) and filter by tag. Draft PR #12 on
branch `feature/tags` (opened 2026-10-15 15:00).

## Open pull requests

| # | Branch | Status | Opened |
| --- | --- | --- | --- |
| 12 | `feature/tags` | Draft | 2026-10-15 15:00 |

## Recreating issues on your own GitHub copy

Forks and template copies do not carry issues or pull requests. If your copy is
on GitHub and the GitHub CLI (`gh`) is installed and logged in, run:

```bash
bash scripts/seed_github.sh
```

It recreates the open issues and the draft PR #12. Merged pull requests such as
#3 cannot be recreated with their dates; this file and `git log` stand in for them.
