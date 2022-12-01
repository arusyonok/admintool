import factory

from accounts import models


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile

    username = factory.Sequence(lambda n: 'user_%d' % n)
    first_name = factory.Sequence(lambda n: 'first_name_%d' % n)
    last_name = factory.Sequence(lambda n: 'last_name_%d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Wallet

    title = factory.Sequence(lambda n: 'wallet_%d' % n)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted is not None:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users.add(user)
