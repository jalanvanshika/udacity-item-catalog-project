# This will add categories and items to the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Category : Dictionary
cat1 = Category(name="Dictionary")
session.add(cat1)
session.commit()


item1 = Item(name="Oxford English Dictionary", description="The Oxford
             English Dictionary.", price="Rs. 499", category=cat1)
session.add(item1)
session.commit()

item2 = Item(name="Webster's Dictionary", description="The dictionary
             by Merriam-Webster is America's most trusted
             online dictionary.", price="Rs. 399", category=cat1)
session.add(item2)
session.commit()


# Category : English Grammar
cat2 = Category(name="English Grammar")
session.add(cat2)
session.commit()


item1 = Item(name="Wren & Martin", description="Wren & Martin refers to a book
             High School English Grammar.", price="Rs. 179", category=cat2)
session.add(item1)
session.commit()

item2 = Item(name="Fundamentals of English Grammar", description="A
             developmental skills text.", price="Rs. 259", category=cat2)
session.add(item2)
session.commit()

# Category : English Literature
cat3 = Category(name="English Literature")
session.add(cat3)
session.commit()


item1 = Item(name="Pride and Prejudice", description="Pride and Prejudice is an
             romantic novel.", price="Rs. 140.99", category=cat3)
session.add(item1)
session.commit()

item2 = Item(name="Emma", description="Emma, by Jane Austen, is a novel
             about youth.", price="Rs. 120.99", category=cat3)
session.add(item2)
session.commit()

# Category : Mathematics
cat4 = Category(name="Mathematics")
session.add(cat4)
session.commit()


item1 = Item(name="Vedic Mathematics", description="Vedic Mathematics is a book
             written by the Indian monk.", price="Rs. 349.99", category=cat4)
session.add(item1)
session.commit()

item2 = Item(name="Concepts of Modern Mathematics",
             description="Concepts of Modern Mathematics is a 1975 book by
             mathematician and science.", price="Rs. 479.99", category=cat4)
session.add(item2)
session.commit()

print("Categories added.")
