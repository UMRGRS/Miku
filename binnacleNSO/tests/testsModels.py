import shutil

from django.test import TestCase
from datetime import date, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from binnacleNSO.models import Profile, Alias, Entry

TEST_DIR = 'media'

# Create your tests here.
class ProfileTestCases(TestCase):
    def testModifyProfileName(self):
        user = Profile.objects.create(name='UMRGRS')
        self.assertEqual(user.name, 'UMRGRS')
        
    def testResetStreakFalse(self):
        user = Profile.objects.create(name='UMRGRS', lastEntryDate=date.today(), streak=10)
        user.resetStreak()
        self.assertEqual(user.streak, 10)
    
    def testResetStreakTrue(self):
        user = Profile.objects.create(name='UMRGRS', lastEntryDate=date.today()-timedelta(days=2), streak=10)
        user.resetStreak()
        self.assertEqual(user.streak, 0)
        
    def testAddEntry(self):
        sub = Alias.objects.create(name='UMRGRS', profile=Profile.objects.create(name='UMRGRS'))
        Entry.objects.create(content='OwO', profile=Profile.objects.get(name='UMRGRS'), alias=sub)
        user = Profile.objects.get(name='UMRGRS')
        self.assertEqual(user.streak, 1)
        self.assertEqual(user.numberOfEntries, 1)
        self.assertEqual(user.lastEntryDate, date.today())
        
class AliasTestCases(TestCase):
    def testCreateAliasNameWithoutPhoto(self):
        sub = Alias.objects.create(name='UMRGRS', profile=Profile.objects.create(name='UMRGRS'))
        self.assertEqual(sub.name, 'UMRGRS')
        self.assertEqual(sub.image, 'media/usersPhotos/default.jpg')
    
    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def testCreateAliasNameWitPhoto(self):
        sub = Alias.objects.create(name='UMRGRS', image=SimpleUploadedFile(name='test_image.jpg', content=open('binnacleNSO/tests/testPhotos/test.jpg', 'rb').read(), content_type='image/jpeg'), profile=Profile.objects.create(name='UMRGRS'))
        self.assertRegex(sub.image.name, '^media/usersPhotos/')
       
class EntriesTestCases(TestCase):
    def testCreateEntryWithoutPhoto(self):
        profile = Profile.objects.create(name='UMRGRS')
        alias = Alias.objects.create(name='UMRGRS', profile=profile)
        entry = Entry.objects.create(content='OwO', profile=profile, alias=alias)
        user = Profile.objects.get(name='UMRGRS')
        self.assertEqual(entry.image, None)
        self.assertEqual(entry.day, user.numberOfEntries)
        self.assertEqual(entry.profile, user)
    
    @override_settings(MEDIA_ROOT=(TEST_DIR))
    def testCreateEntryWithPhoto(self):
        profile = Profile.objects.create(name='UMRGRS')
        alias = Alias.objects.create(name='UMRGRS', profile=profile)
        entry = Entry.objects.create(content='OwO', image=SimpleUploadedFile(name='test_image.jpg', content=open('binnacleNSO/tests/testPhotos/test.jpg', 'rb').read(), content_type='image/jpeg'), profile=profile, alias=alias)
        user = Profile.objects.get(name='UMRGRS')
        self.assertRegex(entry.image.name, '^media/entriesPhotos/')
        self.assertEqual(entry.day, user.numberOfEntries)
        self.assertEqual(entry.profile.name, user.name)
        
def tearDownModule():
    print ('\nDeleting temporary files..\n')
    #shutil.rmtree(TEST_DIR, ignore_errors=True)
    #try:
    #    shutil.rmtree(TEST_DIR)
    #except OSError:
    #    pass