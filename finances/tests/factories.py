import factory
from datetime import datetime

from accounts.tests.factories import ProfileFactory, WalletFactory
from finances import models
from decimal import Decimal


class AbstractRecordFactory(factory.Factory):
    class Meta:
        model = models.AbstractRecord
        abstract = True

    title = "some expense title"
    amount = Decimal("100")
    #date = factory.LazyAttribute(datetime.utcnow())
    #sub_category = 1


class GroupWalletRecordFactory(AbstractRecordFactory):

    class Meta:
        model = models.GroupWalletRecord

    group_wallet = factory.SubFactory(WalletFactory)
    paid_by = factory.SubFactory(ProfileFactory)

    @factory.post_generation
    def paid_for_users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.paid_for_users.add(user)
