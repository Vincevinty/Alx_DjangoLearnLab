# Delete Operation for Book Model

### delete.md
```markdown
## Command
```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
<QuerySet []> #Expected Output