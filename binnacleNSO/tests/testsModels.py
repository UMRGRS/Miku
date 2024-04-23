import shutil

from django.test import TestCase
from datetime import date, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from binnacleNSO.models import Superuser, Subuser, Entry

TEST_DIR = 'test_data'

# Create your tests here.
class SuperuserTestCases(TestCase):
    def testModifySuperuserName(self):
        user = Superuser.objects.create(name='UMRGRS')
        self.assertEqual(user.name, '@UMRGRS')
        
    def testResetStreakFalse(self):
        user = Superuser.objects.create(name='UMRGRS', lastEntryDate=date.today(), streak=10)
        user.resetStreak()
        self.assertEqual(user.streak, 10)
    
    def testResetStreakTrue(self):
        user = Superuser.objects.create(name='UMRGRS', lastEntryDate=date.today()-timedelta(days=2), streak=10)
        user.resetStreak()
        self.assertEqual(user.streak, 0)
        
    def testAddEntry(self):
        sub = Subuser.objects.create(name='UMRGRS', superuser=Superuser.objects.create(name='UMRGRS'))
        Entry.objects.create(content='OwO', subuser=sub)
        user = Superuser.objects.get(name='@UMRGRS')
        self.assertEqual(user.streak, 1)
        self.assertEqual(user.numberOfEntries, 1)
        self.assertEqual(user.lastEntryDate, date.today())
        
class SubuserTestCases(TestCase):
    def testCreateSubuserNameWithoutPhoto(self):
        sub = Subuser.objects.create(name='UMRGRS', superuser=Superuser.objects.create(name='UMRGRS'))
        self.assertEqual(sub.name, '@UMRGRS')
        self.assertEqual(sub.image, 'media/usersPhotos/default.jpg')
    
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media/usersPhotos'))
    def testCreateSubuserNameWitPhoto(self):
        sub = Subuser.objects.create(name='UMRGRS', image=SimpleUploadedFile(name='test_image.jpg', content=open('binnacleNSO/tests/testPhotos/test.jpg', 'rb').read(), content_type='image/jpeg'), superuser=Superuser.objects.create(name='UMRGRS'))
        self.assertRegex(sub.image.name, '^media/usersPhotos/')
       
class EntriesTestCases(TestCase):
    def testCreateEntryWithoutPhoto(self):
        sub = Subuser.objects.create(name='UMRGRS', superuser=Superuser.objects.create(name='UMRGRS'))
        entry = Entry.objects.create(content='OwO', subuser=sub)
        user = Superuser.objects.get(name='@UMRGRS')
        self.assertEqual(entry.image, None)
        self.assertEqual(entry.day, user.numberOfEntries)
        self.assertEqual(entry.subuser.superuser, user)
    
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media/entriesPhotos'))
    def testCreateEntryWithPhoto(self):
        sub = Subuser.objects.create(name='UMRGRS', superuser=Superuser.objects.create(name='UMRGRS'))
        entry = Entry.objects.create(content='OwO', image=SimpleUploadedFile(name='test_image.jpg', content=open('binnacleNSO/tests/testPhotos/test.jpg', 'rb').read(), content_type='image/jpeg'), subuser=sub)
        user = Superuser.objects.get(name='@UMRGRS')
        self.assertRegex(entry.image.name, '^media/entriesPhotos/')
        self.assertEqual(entry.day, user.numberOfEntries)
        self.assertEqual(entry.subuser.superuser, user)
        
def tearDownModule():
    print ('\nDeleting temporary files...\n')
    #shutil.rmtree(TEST_DIR, ignore_errors=True)
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass