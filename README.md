Hey, here’s how to set up and work on the backend project locally.

1. Clone the repository

```bash
git clone https://github.com/SherozMelikov/Backend_FastApi.git
cd Backend_FastApi
```

2. Create virtual environment

Windows CMD:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

5. Run database migrations

```bash
alembic upgrade head
```

6. Run the backend server

```bash
uvicorn app.main:app --reload
```

7. Run tests

```bash
python -m pytest
```

8. Workflow rules

* Do NOT push directly to `main`
* Create your own feature branch

Example:

```bash
git checkout -b feature/your-feature-name
```

9. Push changes

```bash
git add .
git commit -m "Describe your change"
git push -u origin feature/your-feature-name
```

10. Open a Pull Request on GitHub after pushing.

CI tests must pass before merging.
