# Retrieve Operation for Book Model

### retrieve.md
```markdown
## Command
```python
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
('1984', 'George Orwell', 1949) # Expected Output