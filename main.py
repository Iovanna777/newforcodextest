import os
import shutil
import click

from assistant import ocr, database


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path")
@click.option("--client", required=True, help="Client name (FIO)")
def upload(path: str, client: str):
    """Upload a document and extract text."""
    database.init_db()
    case_id = database.get_case_id(client)
    os.makedirs(os.path.join("cases", str(case_id)), exist_ok=True)
    filename = os.path.basename(path)
    dst = os.path.join("cases", str(case_id), filename)
    shutil.copy(path, dst)

    if filename.lower().endswith(".pdf"):
        text = ocr.extract_text_from_pdf(path)
    else:
        text = ocr.extract_text_from_image(path)
    database.add_document(case_id, filename, text)
    click.echo(f"Uploaded {filename} to case {client}")


@cli.command()
@click.option("--client", required=True, help="Client name (FIO)")
def list(client: str):
    """List documents for a client."""
    database.init_db()
    case_id = database.get_case_id(client)
    docs = database.list_documents(case_id)
    for doc_id, fname in docs:
        click.echo(f"{doc_id}: {fname}")


@cli.command()
@click.argument("doc_id", type=int)
def show(doc_id: int):
    """Show extracted text for a document."""
    database.init_db()
    text = database.get_document_text(doc_id)
    click.echo(text)


if __name__ == "__main__":
    cli()
