# coding=utf-8
from elections.tests import VotaInteligenteTestCase as TestCase
from elections.models import Election, Area, Candidate
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.sites.models import Site
from django.test import override_settings


class ElectionsPerAreaTestCase(TestCase):
    def test_an_election_can_have_an_area(self):
        argentina = Area.objects.create(name=u'Argentina')
        election = Election.objects.create(
            name='the name',
            slug='the-slug',
            description='this is a description',
            extra_info_title=u'ver más',
            area=argentina,
            extra_info_content=u'Más Información')

        self.assertIn(election, argentina.elections.all())

    def test_there_is_a_url_with_the_area(self):
        argentina = Area.objects.create(name=u'Argentina')
        url = reverse('area', kwargs={'slug': argentina.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'elections/area.html')

    @override_settings(HIDDEN_AREAS=['argentina'])
    def test_hidden_area(self):
        argentina = Area.objects.create(name=u'Argentina')
        self.assertNotIn(argentina, Area.public.all())

    @override_settings(HIDDEN_AREAS=['argentina'])
    def test_hidden_area_is_still_reachable(self):
        argentina = Area.objects.create(name=u'Argentina')
        url = reverse('area', kwargs={'slug': argentina.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_candidates_per_area(self):
        argentina = Area.objects.create(name=u'Argentina')
        election = Election.objects.create(
            name='the name',
            slug='the-slug',
            description='this is a description',
            extra_info_title=u'ver más',
            area=argentina,
            extra_info_content=u'Más Información')
        c1 = Candidate.objects.create(name='Candidate1')
        c2 = Candidate.objects.create(name='Candidate2')
        c3 = Candidate.objects.create(name='Candidate3')
        election.candidates.add(c1)
        election.candidates.add(c2)
        self.assertIn(c1, argentina.candidates().all())
        self.assertIn(c2, argentina.candidates().all())
        self.assertNotIn(c3, argentina.candidates().all())

    def test_area_ranking(self):
        argentina = Area.objects.create(name=u'Argentina')
        election = Election.objects.create(
            name='the name',
            slug='the-slug',
            description='this is a description',
            extra_info_title=u'ver más',
            area=argentina,
            extra_info_content=u'Más Información')
        c1 = Candidate.objects.create(name='Candidate1')
        c2 = Candidate.objects.create(name='Candidate2')
        c3 = Candidate.objects.create(name='Candidate3')
        election.candidates.add(c1)
        election.candidates.add(c2)
        self.assertIn(c1, election.ranking().all())
        self.assertIn(c2, election.ranking().all())
        self.assertNotIn(c3, election.ranking().all())

    def test_get_position_in_ranking(self):
        argentina = Area.objects.create(name=u'Argentina')
        election = Election.objects.create(
            name='the name',
            slug='the-slug',
            description='this is a description',
            extra_info_title=u'ver más',
            area=argentina,
            extra_info_content=u'Más Información')
        c1 = Candidate.objects.create(name='Candidate1')
        c2 = Candidate.objects.create(name='Candidate2')
        c3 = Candidate.objects.create(name='Candidate3')
        election.candidates.add(c1)
        election.candidates.add(c2)
        self.assertIsNotNone(election.position_in_ranking(c1))
        self.assertIsNotNone(election.position_in_ranking(c2))
        self.assertIsNone(election.position_in_ranking(c3))

        position_c1 = c1.ranking_in_election()
        position_c2 = c2.ranking_in_election()
        position_c3 = c3.ranking_in_election()

        self.assertIsNone(position_c3)
        self.assertEquals(position_c1, election.position_in_ranking(c1))
        self.assertEquals(position_c2, election.position_in_ranking(c2))

class AreaOGPTestCase(TestCase):
    def setUp(self):
        self.argentina = Area.objects.create(name=u'Argentina')
        self.site = Site.objects.get_current()

    def test_get_absolute_url(self):
        url = reverse('area', kwargs={'slug': self.argentina.id})
        self.assertEquals(url, self.argentina.get_absolute_url())

    def test_ogp_things(self):
        self.assertIn(self.argentina.name, self.argentina.ogp_title())
        self.assertEquals('website', self.argentina.ogp_type())
        expected_url = "http://%s%s" % (self.site.domain,
                                        self.argentina.get_absolute_url())
        self.assertEquals(expected_url, self.argentina.ogp_url())
        expected_url = "http://%s%s" % (self.site.domain,
                                        static('img/logo_vi_og.jpg'))
        self.assertEquals(expected_url, self.argentina.ogp_image())

    def test_area_elections_without_position(self):
        election = Election.objects.create(
            name='the name',
            slug='the-slug',
            description='this is a description',
            extra_info_title=u'ver más',
            area=self.argentina,
            position='alcalde',
            extra_info_content=u'Más Información')

        elections_without_position = self.argentina.elections_without_position.all()
        self.assertNotIn(election, elections_without_position)
        self.assertIn(election, self.argentina.elections.all())

