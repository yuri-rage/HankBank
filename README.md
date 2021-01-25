## HankBank
A Flask-SQLAlchemy driven children's allowance manager for families.

Designed to act like a checking/savings account with deposits and withdrawals directly managed by children with transactions shown as "pending" until approved/declined by parents.

Can be hosted on any Flask capable web server.  Built with Raspberry Pi in mind.

Run the init_db.py script to create a blank database in the root directory.  The first user to sign up is designated as the administrator (can be changed later).

Automatic deposits (weekly allowances) should be possible via cron jobs on the server.

### TODO:
* Allow parents to delete transactions
* Maybe tri-state approvals - pending, approved, declined?
* Add a running balance total on the account.html page
* Implement a clean mechanism for automatic/scheduled deposits
* Perhaps break routes.py into smaller chunks
* E-mail notifications?
* Print deposit/withdrawal slips?  Maybe that's too old-fashioned...

-- Yuri - Jan 2021