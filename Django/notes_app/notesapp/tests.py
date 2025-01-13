from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Note


class NotesAPITestCase(APITestCase):
    def setUp(self):
        # Set up initial data for testing
        self.note1 = Note.objects.create(
            title="Test Note 1",
            body="This is a test note.",
            category="BUSINESS"
        )
        self.note2 = Note.objects.create(
            title="Test Note 2",
            body="Another test note.",
            category="PERSONAL"
        )
        self.list_url = reverse("notes")  # URL for listing and creating notes
        self.detail_url = lambda slug: reverse("notes_detail", args=[slug])  # Detail URL

    def test_get_notes_list(self):
        """Test retrieving a list of notes."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check the number of returned notes
        self.assertEqual(response.data[0]["title"], self.note1.title)

    def test_create_note(self):
        """Test creating a new note."""
        data = {
            "title": "New Note",
            "body": "This is a new note.",
            "category": "IMPORTANT"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertIsNotNone(response.data["slug"])  # Check if the slug was generated

    def test_get_note_detail(self):
        """Test retrieving a single note."""
        response = self.client.get(self.detail_url(self.note1.slug))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.note1.title)

    def test_update_note(self):
        """Test updating an existing note."""
        data = {
            "title": "Updated Note Title",
            "body": "Updated body text.",
            "category": "BUSINESS"
        }
        response = self.client.put(self.detail_url(self.note1.slug), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])

    def test_delete_note(self):
        """Test deleting a note."""
        response = self.client.delete(self.detail_url(self.note1.slug))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(slug=self.note1.slug).exists())

    def test_note_not_found(self):
        """Test accessing a non-existent note."""
        response = self.client.get(self.detail_url("non-existent-slug"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
