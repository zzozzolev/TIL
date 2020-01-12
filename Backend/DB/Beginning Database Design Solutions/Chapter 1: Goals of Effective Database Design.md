- 프로그램과 마찬가지로 디비 디자인을 잘못하면 폭망 가능.

## CRUD
- CRUD stands for the four fundamental database operations that any database should provide: Create, Read, Update, and Delete.

## Retrieval
- Retrieval is another word for ‘‘read,’’ the R in CRUD. The database should allow you to find every piece of data.
- Being able to find all of the data in the database quickly and reliably is an important part of database design. Finding the data you need in a poorly designed database can take hours or days instead of mere seconds.

## Consistency
- Another aspect of the R in CRUD is consistency. The database should provide consistent results.
- Consistency means different parts of the database don’t hold contradictory views of the same information.
- A well-built database product can ensure that the exact same query returns the same result but design also plays an important role. If the database is poorly designed, you may be able to store conflicting data in different parts of the database.

## Validity
- Validity is closely related to the idea of consistency.
- Validity means data is validated where possible against other pieces of data in the database.

## Easy Error Correction
- Easy correction of errors is a built-in feature of computerized databases, but to get the best advantage from this feature you need a good design. If order information is contained in a free-formatted text section, the database will have trouble fixing typos. If you put the product name in a separate field, the database can make this change easily.

## Speed
- An important aspect of all of the CRUD components is speed. A well-designed database can create, read, update, and delete records quickly.
- Good design plays a critical role in database efficiency. A poorly organized database may still be faster than the paper equivalent but it will be a lot slower than a well-designed database.

## Atomic Transactions
- Recall that an atomic transaction is a possibly complex series of actions that is considered as a single operation by those not involved directly in performing the transaction.
- The transaction either happens completely or none of its pieces happen — it cannot happen halfway.
- Atomic transactions are important for maintaining consistency and validity, and are thus important for the R and U parts of CRUD.
- You can then either commit the transaction to make the changes permanent or rollback the transaction to undo them all and restore the database to the state it had before you started the transaction.

## ACID
- ACID is an acronym describing four features that an effective transaction system should provide. ACID stands for Atomicity, Consistency, Isolation, and Durability.
- Atomicity means transactions are atomic. The operations in a transaction either all happen or none of them happen.
- Consistency means the transaction ensures that the database is in a consistent state before and after the transaction. In other words, if the operations within the transaction would violate the database’s rules, the transaction is rolled back.
- Isolation means the transaction isolates the details of the transaction from everyone except the person making the transaction.
- In particular, two transactions operate in isolation and cannot interfere with each other.
- Durability means that once a transaction is committed, it will not disappear later. If the power fails, when the database restarts, the effects of this transaction will still be there.
- To provide durability, the database cannot consider the transaction as committed until its changes are shadowed or recorded in the log so the database will not lose the changes if it crashes.

## Persistence and Backups
- To protect against this sort of trouble, you need to perform regular backups.
- You can back up the database daily.
- Many higher-end database products allow you to shadow every database operation as it occurs so you always have a complete copy of everything that happens.
- It’s always best to store backups away from the computer that you’re backing up.
- A backup doesn’t do much good if you can’t use it!
- Exactly how you implement database backups depends on several factors such as how likely you think a problem will be, how quickly you need to recover from it, and how disastrous it would be to lose some data and spend time to restore from a backup.

## Low Cost and Extensibility
- Ideally the database should be easy to obtain and install, inexpensive, and easily extensible.

## Ease of Use
- Those sophisticated users can easily understand the database, they can build better user interfaces for the less advanced users.

## Portability
- It allows you to access the data from anywhere you have access to the Web.

## Security
- If you separate the data into categories that different types of users need to manipulate, you can grant different levels of permission to the different kinds of users.

## Sharing
- Breaking the data into reasonable pieces can also help coordinate among multiple users.
- Grouping the data appropriately lets you lock the smallest amount of data possible so more data is available for other users
to edit.