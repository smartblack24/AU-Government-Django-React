import { gql } from 'react-apollo';
import * as fragments from 'fragments';

export const createOrganisationMutation = gql`
  mutation createOrganisation($organisationData: OrganisationInput!) {
    createOrganisation(organisationData: $organisationData) {
      errors
      organisation {
        ...Organisation
      }
    }
  }
  ${fragments.organisationFragment}
`;
