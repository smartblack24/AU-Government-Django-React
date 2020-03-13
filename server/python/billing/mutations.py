from datetime import datetime
from decimal import Decimal

import graphene
from accounts.models import Client, Contact, User
from sitename.utils import check_for_existence
from core.models import MatterType as MatterTypeModel
from core.models import MatterStatus, LeadStatus
from dateutil import parser
from graphql_relay.node.node import from_global_id

from .inputs import MatterInput, TimeEntryInput
from .models import Matter, Note, TimeEntry, EntryType
from core.models import TimeEntryType as TimeRecord
from .schema import MatterType, NoteType, TimeEntryType


class LostMatterMutation(graphene.Mutation):
    class Arguments:
        matter_id = graphene.ID(required=True)

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        matter_id = args.get('matter_id')
        errors = []
        matter = None

        try:
            matter_id = from_global_id(matter_id)[1]
            matter = Matter.objects.get(pk=matter_id)
        except Exception as e:
            errors.append(str(e))
            return LostMatterMutation(errors=errors)
        matter.billable_status = 3
        matter.lead_status = LeadStatus.objects.get(name="Lost")
        matter.matter_status = MatterStatus.objects.get(name="Matter Closed")
        matter.closed_date = datetime.now()
        matter.save()
        return LostMatterMutation(errors=errors)


class WinMatterMutation(graphene.Mutation):
    class Arguments:
        matter_id = graphene.ID(required=True)

    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, **args):
        matter_id = args.get('matter_id')
        errors = []
        matter = None

        try:
            matter_id = from_global_id(matter_id)[1]
            matter = Matter.objects.get(pk=matter_id)
        except Exception as e:
            errors.append(str(e))
            return LostMatterMutation(errors=errors)
        matter.entry_type = EntryType.objects.get(id=1)
        matter.lead_status = LeadStatus.objects.get(name="Won")
        date = datetime.now().strftime("%Y-%m-%d")
        matter.created_date = parser.parse(date)
        matter.is_conflict_check_sent = False
        matter.save()
        return LostMatterMutation(errors=errors)


class UpdateMatterMutation(graphene.Mutation):
    class Arguments:
        matter_id = graphene.ID(required=True)
        matter_data = MatterInput(required=True)

    errors = graphene.List(graphene.String)
    matter = graphene.Field(lambda: MatterType)

    @staticmethod
    def mutate(root, info, **args):
        matter_data = args.get('matter_data')
        errors = []
        matter = None

        try:
            check_for_existence(
                (args.get('matter_id'), Matter),
                (matter_data.client.id, Client),
                (matter_data.principal.id, User),
                (matter_data.manager.id, User),
                (matter_data.matter_type.id, MatterTypeModel),
            )
        except Exception as e:
            errors.append(str(e))
            return UpdateMatterMutation(errors=errors, matter=None)

        matter_id = from_global_id(args.get('matter_id'))[1]
        matter = Matter.objects.get(pk=matter_id)
        if matter.entry_type.id == 1:
            matter.update(
                exclude=[
                    'budget',
                    'closed_date',
                    'billable_status',
                    'assistant',
                    'matter_status',
                    'lead_status',
                    'entry_type'
                    ],
                **matter_data
            )

            try:
                assistant_id = from_global_id(matter_data.assistant.id)[1]
                assistant = User.objects.get(pk=assistant_id)
                matter.assistant = assistant
            except (User.DoesNotExist, AttributeError):
                matter.assistant = None

            if matter_data.closed_date:
                try:
                    matter.closed_date = parser.parse(matter_data.closed_date)
                except TypeError:
                    pass
            else:
                matter.closed_date = None

            if matter_data.billable_status is 3 and not matter.may_close:
                errors.append('The matter cannot be closed!')
            elif matter_data.billable_status is 3:
                matter.billable_status = matter_data.billable_status
                matter.closed_date = datetime.now()
            else:
                matter.billable_status = matter_data.billable_status

            matter.budget = matter_data.budget or 0
            if matter_data.matter_status:
                matter.matter_status = MatterStatus.objects.get(
                    id=matter_data.matter_status)
        elif matter.entry_type.id == 2:
            matter.update(
                exclude=[
                    'budget',
                    'closed_date',
                    'billable_status',
                    'assistant',
                    'matter_status',
                    'lead_status',
                    'lead_date',
                    'entry_type'
                    ],
                **matter_data
            )

            try:
                assistant_id = from_global_id(matter_data.assistant.id)[1]
                assistant = User.objects.get(pk=assistant_id)
                matter.assistant = assistant
            except (User.DoesNotExist, AttributeError):
                matter.assistant = None

            if matter_data.closed_date:
                try:
                    matter.closed_date = parser.parse(matter_data.closed_date)
                except TypeError:
                    pass
            else:
                matter.closed_date = None
            if matter_data.lead_date:
                matter.lead_date = parser.parse(matter_data.lead_date)
            matter.budget = matter_data.budget or 0
            if matter_data.lead_status:
                matter.lead_status = LeadStatus.objects.get(
                    id=matter_data.lead_status)
        matter.save()
        return UpdateMatterMutation(errors=errors, matter=matter)


class CreateMatterMutation(graphene.Mutation):
    class Arguments:
        matter_data = MatterInput(required=True)

    errors = graphene.List(graphene.String)
    matter = graphene.Field(lambda: MatterType)

    @staticmethod
    def mutate(root, info, **args):
        matter_data = args.get('matter_data')
        errors = []
        matter = None

        matter = Matter()
        try:
            check_for_existence(
                (matter_data.client.id, Client),
                (matter_data.principal.id, User),
                (matter_data.manager.id, User),
                (matter_data.matter_type.id, MatterTypeModel),
            )
        except Exception as e:
            errors.append(str(e))
            return UpdateMatterMutation(errors=errors, matter=None)

        matter = Matter()
        if matter_data.entry_type == 1:
            matter.update(exclude=[
                'budget',
                'assistant',
                'closed_date',
                'matter_status',
                'entry_type'
                ],
                **matter_data)
            matter.entry_type = EntryType.objects.get(id=1)
            matter.lead_status = LeadStatus.objects.get(name="Won")
            if matter_data.matter_status:
                matter.matter_status = MatterStatus.objects.get(
                    id=matter_data.matter_status
                )
            if matter_data.assistant:
                try:
                    assistant_id = from_global_id(matter_data.assistant.id)[1]
                    assistant = User.objects.get(pk=assistant_id)
                    matter.assistant = assistant
                except User.DoesNotExist:
                    matter.assistant = None

            try:
                matter.closed_date = parser.parse(matter_data.closed_date)
            except TypeError:
                pass
            matter.budget = matter_data.budget or 0

        elif matter_data.entry_type == 2:
            matter.update(exclude=[
                'budget',
                'assistant',
                'closed_date',
                'matter_status',
                'lead_status',
                'entry_type',
                'created_date',
                ],
                **matter_data)
            matter.entry_type = EntryType.objects.get(id=2)
            # matter.billable_status = 1
            if not matter_data.lead_date:
                matter.lead_date = datetime.now()

            if matter_data.assistant:
                try:
                    assistant_id = from_global_id(
                        matter_data.assistant.id
                        )[1]
                    assistant = User.objects.get(pk=assistant_id)
                    matter.assistant = assistant
                except User.DoesNotExist:
                    matter.assistant = None

            try:
                matter.closed_date = parser.parse(matter_data.closed_date)
            except TypeError:
                pass
            if matter_data.lead_status:
                matter.lead_status = LeadStatus.objects.get(
                    id=matter_data.lead_status
                    )
            matter.budget = matter_data.budget or 0
            matter.entry_type = EntryType.objects.get(id=2)

        matter.save()
        return CreateMatterMutation(errors=errors, matter=matter)


class CreateTimeEntryMutation(graphene.Mutation):
    class Arguments:
        entry_type = graphene.Int()
        time_entry_data = TimeEntryInput()

    errors = graphene.List(graphene.String)
    time_entry = graphene.Field(lambda: TimeEntryType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        time_entry_data = args.get('time_entry_data')
        entry_type = args.get('entry_type')
        time_entry = None

        try:
            check_for_existence(
                (time_entry_data.client.id, Client),
                (time_entry_data.matter.id, Matter),
                (time_entry_data.staff_member.id, User),
            )
        except Exception as e:
            errors.append(str(e))
            return CreateTimeEntryMutation(errors=errors)
        time_entry_type = TimeRecord.objects.get(
            id=int(time_entry_data.record_type)
            )
        print(time_entry_data.date)
        date = datetime.combine(
            parser.parse(time_entry_data.date),
            datetime.strptime(time_entry_data.time, '%I:%M %p').time()
            )
        if time_entry_data.status == 1:
            time_entry = TimeEntry(
                entry_type=entry_type,
                units_to_bill=time_entry_data.units,
                time_entry_type=time_entry_type,
                date=date
            )
        else:
            time_entry = TimeEntry(
                entry_type=entry_type,
                units_to_bill=0,
                time_entry_type=time_entry_type,
                date=date
            )
        time_entry.update(exclude=['rate', 'date'], **time_entry_data)
        staff_member_id = from_global_id(time_entry_data.staff_member.id)[1]
        staff = User.objects.get(pk=staff_member_id)

        if time_entry_data.rate == staff.rate:
            time_entry.rate = Decimal(staff.rate)
        else:
            time_entry.rate = Decimal(time_entry_data.rate)

        time_entry.save()

        return CreateTimeEntryMutation(errors=errors, time_entry=time_entry)


class UpdateTimeEntryMutation(graphene.Mutation):
    class Arguments:
        time_entry_id = graphene.ID()
        time_entry_data = TimeEntryInput()

    errors = graphene.List(graphene.String)
    time_entry = graphene.Field(lambda: TimeEntryType)

    @staticmethod
    def mutate(root, info, **args):
        errors = []
        time_entry_data = args.get('time_entry_data')
        try:
            check_for_existence(
                (time_entry_data.client.id, Client),
                (time_entry_data.matter.id, Matter),
                (time_entry_data.staff_member.id, User),
                (args.get('time_entry_id'), TimeEntry),
            )
        except Exception as e:
            errors.append(str(e))
            return UpdateTimeEntryMutation(errors=errors)

        time_entry_id = from_global_id(args.get('time_entry_id'))[1]

        time_entry = TimeEntry.objects.get(pk=time_entry_id)

        time_entry.update(
            exclude=['rate', 'time_entry_type', 'date'],
            **time_entry_data
            )
        date = datetime.combine(
            parser.parse(time_entry_data.date),
            datetime.strptime(time_entry_data.time, '%I:%M %p').time()
            )

        time_entry.date = date
        if time_entry_data.status == 1:
            time_entry.units_to_bill = time_entry_data.units
        else:
            time_entry.units_to_bill = 0

        staff_member_id = from_global_id(time_entry_data.staff_member.id)[1]
        staff = User.objects.get(pk=staff_member_id)

        if time_entry_data.rate == staff.rate:
            time_entry.rate = Decimal(staff.rate)
        else:
            time_entry.rate = Decimal(time_entry_data.rate)

        time_entry.save()

        return UpdateTimeEntryMutation(errors=errors, time_entry=time_entry)


class CreateNoteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        text = graphene.String(required=True)
        user_id = graphene.ID(required=True)
        date_time = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    note = graphene.Field(lambda: NoteType)

    @staticmethod
    def mutate(root, info, **args):
        id = args.get('id')
        text = args.get('text')
        user_id = args.get('user_id')
        errors = []
        note = None

        if not text:
            errors.append('Note text must be specified')

        if not errors:
            user_id = from_global_id(user_id)[1]
            contact = None
            matter = None

            matter_id = from_global_id(id)[1]
            try:
                matter = Matter.objects.get(pk=matter_id)
            except Matter.DoesNotExist:
                contact_id = from_global_id(id)[1]
                try:
                    contact = Contact.objects.get(pk=contact_id)
                except Contact.DoesNotExist:
                    errors.append('Contact with the provided id does not exist')
                    return CreateNoteMutation(errors=errors, note=note)

            note = Note.objects.create(
                matter=matter,
                contact=contact,
                text=text,
                date_time=parser.parse(args.get('date_time')),
                user_id=user_id,
            )

            return CreateNoteMutation(errors=errors, note=note)


class UpdateNoteMutation(graphene.Mutation):
    class Arguments:
        note_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        text = graphene.String(required=True)
        date_time = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    note = graphene.Field(lambda: NoteType)

    @staticmethod
    def mutate(root, info, **args):
        note_id = args.get('note_id')
        user_id = from_global_id(args.get('user_id'))[1]
        errors = []
        note = None

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            errors.append('User does not exist!')

        if not note_id:
            errors.append('Note id must be specified')

        if not errors:
            try:
                note = Note.objects.get(pk=note_id)
            except Note.DoesNotExist:
                errors.append('Note with the provided id does not exist')
                return UpdateNoteMutation(errors=errors, note=note)

            note.text = args.get('text')
            note.user = user
            note.date_time = parser.parse(args.get('date_time'))
            note.save()

        return UpdateNoteMutation(errors=errors, note=note)
