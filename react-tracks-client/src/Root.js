import React from "react";
import withRoot from "./withRoot";
import { Query } from 'react-apollo'
import { gql } from 'apollo-boost'

const Root = () => (
    <Query query={GET_TRACKS_QUERY}>
        {({ data, loading, error }) => {
                if (loading) return <div>Loading...</div>
                if (error) return <div>{ error.message }</div>
                return <div>{ JSON.stringify(data) }</div>
            }
        }
    </Query>
)

const GET_TRACKS_QUERY = gql`
    {
        tracks {
            id
            title
            url
            description
        }
    }
`

export default withRoot(Root);
