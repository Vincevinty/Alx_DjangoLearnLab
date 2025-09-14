# Update Operation for Book Model

### update.md
```markdown
## Command
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
'Nineteen Eighty-Four' #Expected Output