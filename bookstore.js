// Step 2: switch to the bookstore database
// use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json (drop first so reruns do not duplicate authors)
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
printjson(db.authors.find().toArray())
printjson(db.books.find().toArray())

// Step 6: insert two new books (author_004 is a new author, author_002 already exists)
db.books.insertMany([
  {
    title: "The Great Gatsby",
    published_year: 1925,
    author_ids: ["author_004"]
  },
  {
    title: "Coraline",
    published_year: 2002,
    author_ids: ["author_002"]
  }
])

// Step 7: add missing authors (author_004 is referenced above but not yet in authors)
db.authors.insertOne({
  _id: "author_004",
  name: "F. Scott Fitzgerald",
  nationality: "American",
  bio: {
    short: "American novelist of the Jazz Age.",
    long: "F. Scott Fitzgerald was an American novelist and short story writer whose work captured the glamour and excess of the 1920s Jazz Age. He is best known for The Great Gatsby, a portrait of wealth and longing on Long Island."
  }
})

// Step 8: filter books by a list of authors (one loaded author, one new author)
printjson(db.books.find({ author_ids: { $in: ["author_001", "author_004"] } }).toArray())
