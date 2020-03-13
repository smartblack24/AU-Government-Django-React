import pytest

from accounts.factories import LocationFactory

from ..factories import (DocumentFactory, SectionFactory, OccupationFactory,
                         OfficeFactory, MatterTypeFactory, IndustryFactory,
                         MatterSubTypeFactory, InvoiceStatusFactory,
                         MatterStatusFactory, DocumentTypeFactory,
                         GeneralFactory, PdfFactory)


@pytest.mark.django_db
def test_str_method_in_model():
    """ Test str methods in core models """

    name = 'instance_name'
    factories = [MatterSubTypeFactory, OccupationFactory,    IndustryFactory,
                 MatterStatusFactory,  InvoiceStatusFactory, MatterTypeFactory,
                 DocumentTypeFactory,  PdfFactory]

    for factory in factories:
        instance = factory.__call__(name=name)
        assert str(instance) == instance.name

    document = DocumentFactory(id=25)
    assert str(document) == str(document.id)

    general_str = "General Configuration"
    general = GeneralFactory()
    assert str(general) == general_str

    section = SectionFactory(number='6666')
    assert str(section) == section.number

    #  Tests for PDF model
    pdf = PdfFactory(name='name_pdf')
    assert str(pdf) == pdf.name
    assert pdf.get_full_name() == pdf.name

    #  Tests for Offices model
    location_suburb = LocationFactory(suburb='Sydney')
    office = OfficeFactory(location=location_suburb)
    assert str(office) == location_suburb.suburb

    location_address1 = LocationFactory(suburb=None, address1='address_first')
    office = OfficeFactory(location=location_address1)
    assert str(office) == location_address1.address1

    office_str = 'No location'
    office = OfficeFactory(location=None)
    assert str(office) == office_str


@pytest.mark.django_db
def test_get_branding_theme_id_from_xero_method():
    """ Test get branding theme id from xero offices method """

    office = OfficeFactory()
    assert office.get_branding_theme_id_from_xero() is False
