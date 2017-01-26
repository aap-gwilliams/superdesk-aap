module.exports = function() {
    return {
        defaultRoute: '/workspace',

        workspace: {
            ingest: 1,
            content: 1,
            tasks: 0
        },

        editor: {
            toolbar: false,
            embeds: false,
            paste: {
                forcePlainText: true,
                cleanPastedHTML: false
            }
        },

        features: {
            elasticHighlight: 1,
            swimlane: {columnsLimit: 4},
            editFeaturedImage: 1,
            confirmMediaOnUpdate: 1,
            hideLiveSuggestions: 1
        },

        view: {
            timeformat: 'HH:mm',
            dateformat: 'DD/MM/YYYY'
        },

        search: {
            slugline: 1, headline: 1, unique_name: 1, story_text: 1,
            byline: 1, keywords: 1, creator: 1, from_desk: 1,
            to_desk: 1, spike: 1, scheduled: 1, company_codes: 1,
            useDefaultTimezone: 1, ingest_provider: 1, raw_search: 1,
            featuremedia: 1
        },
        
        previewFormats: [{
            name: 'AAPIpNewsFormatter',
            outputType: 'json',
            outputField: 'article_text'
        }],

        defaultTimezone: 'Australia/Sydney',
        shortDateFormat: 'DD/MM',
        ArchivedDateFormat: 'D/MM/YYYY',

        list: {
            'priority': [
                'urgency',
                'priority'
            ],
            'firstLine': [
                'slugline',
                'highlights',
                'associations',
                'takekey',
                'state',
                'update',
                'takepackage',
                 'embargo',
                'flags',
                'updated',
                'headline',
		'markedDesks',
                'wordcount',
                'provider',
                'versioncreator',
                'versioncreated'
            ],
            'narrowView': [
                'slugline',
                'takekey',
                'state',
                'provider',
                'versioncreated'
            ],
            'thinRows': true
        },

        langOverride: {
            'en': {
                "Advanced Search": "Advanced",
                "URGENCY": "NEWS VALUE",
                "Urgency": "News Value",
                "urgency": "news value",
                "Urgency stats": "News Value stats",
                "SERVICE": "CATEGORY",
                "SERVICES": "CATEGORIES",
                "Services": "Categories",
                "Service": "Category",
                "Mar": "March",
                "Apr": "April",
                "Jun": "June",
                "Jul": "July",
                "Sep": "Sept"        
            },

            'en_GB': {
                "Advanced Search": "Advanced",
                "URGENCY": "NEWS VALUE",
                "Urgency": "News Value",
                "urgency": "news value",
                "Urgency stats": "News Value stats",
                "SERVICE": "CATEGORY",
                "SERVICES": "CATEGORIES",
                "Services": "Categories",
                "Service": "Category",
                "Mar": "March",
                "Apr": "April",
                "Jun": "June",
                "Jul": "July",
                "Sep": "Sept"
            },

            'en_US': {
                "Advanced Search": "Advanced",
                "URGENCY": "NEWS VALUE",
                "Urgency": "News Value",
                "urgency": "news value",
                "Urgency stats": "News Value stats",
                "SERVICE": "CATEGORY",
                "SERVICES": "CATEGORIES",
                "Services": "Categories",
                "Service": "Category",
                "Mar": "March",
                "Apr": "April",
                "Jun": "June",
                "Jul": "July",
                "Sep": "Sept"
            },

            'en_AU': {
                "Advanced Search": "Advanced",
                "URGENCY": "NEWS VALUE",
                "Urgency": "News Value",
                "urgency": "news value",
                "Urgency stats": "News Value stats",
                "SERVICE": "CATEGORY",
                "SERVICES": "CATEGORIES",
                "Services": "Categories",
                "Service": "Category",
                "Mar": "March",
                "Apr": "April",
                "Jun": "June",
                "Jul": "July",
                "Sep": "Sept"
            }
        }
    };
};
