# This will add categories and items to the database 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Category : Dictionary
cat1 = Category(name = "Dictionary")
session.add(cat1)
session.commit()


item1 = Item(name = "Oxford English Dictionary", description = "DescriptionThe Oxford English Dictionary is the principal historical dictionary of the English language, published by Oxford University Press.", price = "Rs. 499", category = cat1)
session.add(item1)
session.commit()

item2 = Item(name = "Webster's Dictionary", description = "he dictionary by Merriam-Webster is America's most trusted online dictionary for English word definitions, meanings, and pronunciation.", price = "Rs. 399", category = cat1)
session.add(item2)
session.commit()



#Category : English Grammar
cat2 = Category(name = "English Grammar")
session.add(cat2)
session.commit()


item1 = Item(name = "Wren & Martin", description = "Wren & Martin refers to a single book High School English Grammar and Composition or collectively, a series of English grammar textbooks.", price = "Rs. 179", category = cat2)
session.add(item1)
session.commit()

item2 = Item(name = "Fundamentals of English Grammar", description = "A classic developmental skills text for lower-intermediate and intermediate English language learners, Fundamentals of English Grammar is a comprehensive reference grammar.", price = "Rs. 259", category = cat2)
session.add(item2)
session.commit()


#Category : English Literature
cat3 = Category(name = "English Literature")
session.add(cat3)
session.commit()


item1 = Item(name = "Pride and Prejudice", description = "Pride and Prejudice is an 1813 romantic novel by Jane Austen.", price = "Rs. 140.99", category = cat3)
session.add(item1)
session.commit()

item2 = Item(name = "Emma", description = "Emma, by Jane Austen, is a novel about youthful hubris and the perils of misconstrued romance. ", price = "Rs. 120.99", category = cat3)
session.add(item2)
session.commit()


#Category : Mathematics
cat4 = Category(name = "Mathematics")
session.add(cat4)
session.commit()


item1 = Item(name = "Vedic Mathematics", description = "Vedic Mathematics is a book written by the Indian monk Swami Bharati Krishna Tirtha and first published in 1965.", price = "Rs. 349.99", category = cat4)
session.add(item1)
session.commit()

item2 = Item(name = "Concepts of Modern Mathematics", description = "Concepts of Modern Mathematics is a 1975 book by mathematician and science popularizer Ian Stewart about recent developments in mathematics.", price = "Rs. 479.99", category = cat4)
session.add(item2)
session.commit()


print("Categories added.")


