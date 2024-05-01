from reviewboard.reviews.models import GeneralComment
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import (
    review_reply_general_comment_item_mimetype,
    review_reply_general_comment_list_mimetype)
from reviewboard.webapi.tests.mixins import (
    BasicTestsMetaclass,
    ReviewRequestChildItemMixin,
    ReviewRequestChildListMixin)
from reviewboard.webapi.tests.mixins_comment import (
    CommentReplyItemMixin,
    CommentReplyListMixin)
from reviewboard.webapi.tests.urls import (
    get_review_reply_general_comment_item_url,
    get_review_reply_general_comment_list_url)


class ResourceListTests(CommentReplyListMixin, ReviewRequestChildListMixin,
                        BaseWebAPITestCase, metaclass=BasicTestsMetaclass):
    """Testing the ReviewReplyGeneralCommentResource list APIs."""
    fixtures = ['test_users']
    sample_api_url = \
        'review-requests/<id>/reviews/<id>/replies/<id>/general-comments/'
    resource = resources.review_reply_general_comment

    def setup_review_request_child_test(self, review_request):
        review = self.create_review(review_request, user=self.user,
                                    publish=True)
        self.create_general_comment(review)
        reply = self.create_reply(review, user=self.user)

        return (get_review_reply_general_comment_list_url(reply),
                review_reply_general_comment_list_mimetype)

    def setup_http_not_allowed_item_test(self, user):
        review_request = self.create_review_request(
            submitter=user,
            publish=True)
        review = self.create_review(review_request, user=user)
        self.create_general_comment(review)
        reply = self.create_reply(review, user=user)

        return get_review_reply_general_comment_list_url(reply)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp['id'], comment.pk)
        self.assertEqual(item_rsp['text'], comment.text)

        if comment.rich_text:
            self.assertEqual(item_rsp['text_type'], 'markdown')
        else:
            self.assertEqual(item_rsp['text_type'], 'plain')

    #
    # HTTP GET tests
    #

    def setup_basic_get_test(self, user, with_local_site, local_site_name,
                             populate_items):
        review_request = self.create_review_request(
            with_local_site=with_local_site,
            submitter=user,
            publish=True)
        review = self.create_review(review_request, user=user)
        comment = self.create_general_comment(review)
        reply = self.create_reply(review, user=user)

        if populate_items:
            items = [
                self.create_general_comment(reply, reply_to=comment),
            ]
        else:
            items = []

        return (get_review_reply_general_comment_list_url(reply,
                                                          local_site_name),
                review_reply_general_comment_list_mimetype,
                items)

    #
    # HTTP POST tests
    #

    def setup_basic_post_test(self, user, with_local_site, local_site_name,
                              post_valid_data):
        review_request = self.create_review_request(
            with_local_site=with_local_site,
            submitter=user,
            publish=True)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_general_comment(review)
        reply = self.create_reply(review, user=user)

        return (
            get_review_reply_general_comment_list_url(reply, local_site_name),
            review_reply_general_comment_item_mimetype,
            {
                'reply_to_id': comment.pk,
                'text': 'Test comment',
            },
            [reply, comment])

    def check_post_result(self, user, rsp, reply, comment):
        reply_comment = \
            GeneralComment.objects.get(pk=rsp['general_comment']['id'])
        self.assertEqual(reply_comment.text, 'Test comment')
        self.assertEqual(reply_comment.reply_to, comment)
        self.assertEqual(reply_comment.rich_text, False)
        self.compare_item(rsp['general_comment'], reply_comment)

    def test_post_with_http_303(self):
        """Testing the POST
        review-requests/<id>/reviews/<id>/replies/<id>/general-comments/ API
        with second instance of same reply
        """
        comment_text = "My Comment Text"

        review_request = self.create_review_request(publish=True)
        review = self.create_review(review_request, user=self.user,
                                    publish=True)
        comment = self.create_general_comment(review)
        reply = self.create_reply(review, user=self.user)
        reply_comment = self.create_general_comment(reply, reply_to=comment)

        # Now post another reply to the same comment in the same review.
        rsp = self.api_post(
            get_review_reply_general_comment_list_url(reply),
            {
                'reply_to_id': comment.pk,
                'text': comment_text
            },
            expected_status=303,
            expected_mimetype=review_reply_general_comment_item_mimetype)

        self.assertEqual(rsp['stat'], 'ok')

        reply_comment = GeneralComment.objects.get(
            pk=rsp['general_comment']['id'])
        self.assertEqual(reply_comment.text, comment_text)


class ResourceItemTests(CommentReplyItemMixin, ReviewRequestChildItemMixin,
                        BaseWebAPITestCase, metaclass=BasicTestsMetaclass):
    """Testing the ReviewReplyGeneralCommentResource item APIs."""
    fixtures = ['test_users']
    sample_api_url = ('review-requests/<id>/reviews/<id>/replies/<id>/'
                      'general-comments/<id>/')
    resource = resources.review_reply_general_comment

    def setup_review_request_child_test(self, review_request):
        review = self.create_review(review_request, user=self.user,
                                    publish=True)
        comment = self.create_general_comment(review)
        reply = self.create_reply(review, user=self.user)
        reply_comment = self.create_general_comment(reply, reply_to=comment)

        return (get_review_reply_general_comment_item_url(reply,
                                                          reply_comment.pk),
                review_reply_general_comment_item_mimetype)

    def setup_http_not_allowed_list_test(self, user):
        review_request = self.create_review_request(
            submitter=user,
            publish=True)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_general_comment(review)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_general_comment(reply, reply_to=comment)

        return get_review_reply_general_comment_item_url(
            reply, reply_comment.pk)

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp['id'], comment.pk)
        self.assertEqual(item_rsp['text'], comment.text)

        if comment.rich_text:
            self.assertEqual(item_rsp['text_type'], 'markdown')
        else:
            self.assertEqual(item_rsp['text_type'], 'plain')

    #
    # HTTP DELETE tests
    #

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(
            with_local_site=with_local_site,
            submitter=user,
            publish=True)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_general_comment(review)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_general_comment(reply, reply_to=comment)

        return (
            get_review_reply_general_comment_item_url(
                reply, reply_comment.pk, local_site_name),
            [reply_comment, reply]
        )

    def check_delete_result(self, user, reply_comment, reply):
        self.assertNotIn(reply_comment, reply.general_comments.all())

    #
    # HTTP GET tests
    #

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(
            with_local_site=with_local_site,
            submitter=user,
            publish=True)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_general_comment(review)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_general_comment(reply, reply_to=comment)

        return (
            get_review_reply_general_comment_item_url(
                reply, reply_comment.pk, local_site_name),
            review_reply_general_comment_item_mimetype,
            reply_comment
        )

    #
    # HTTP PUT tests
    #

    def setup_basic_put_test(self, user, with_local_site, local_site_name,
                             put_valid_data):
        review_request = self.create_review_request(
            with_local_site=with_local_site,
            submitter=user,
            publish=True)
        review = self.create_review(review_request, user=user, publish=True)
        comment = self.create_general_comment(review)
        reply = self.create_reply(review, user=user)
        reply_comment = self.create_general_comment(reply, reply_to=comment)

        return (
            get_review_reply_general_comment_item_url(
                reply, reply_comment.pk, local_site_name),
            review_reply_general_comment_item_mimetype,
            {
                'text': 'Test comment',
            },
            reply_comment,
            [])

    def check_put_result(self, user, item_rsp, comment, *args):
        comment = GeneralComment.objects.get(pk=comment.pk)
        self.assertEqual(item_rsp['id'], comment.pk)
        self.assertEqual(item_rsp['text'], 'Test comment')
        self.assertEqual(comment.text, 'Test comment')
