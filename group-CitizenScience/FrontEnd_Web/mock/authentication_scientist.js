import Mock from 'mockjs'

const assistant_data = Mock.mock({
    'items|10': [{
        'account_id|100000-999999': 666666,
        name: '@sentence(2, 3)',
        display_time: '@datetime',
        remarks: '@sentence(10,20)'
    }]
})

export default [
    {
        url: '/vue-admin-template/authentication_scientist/list',
        type: 'get',
        response: config => {
            const items = assistant_data.items
            return {
                code: 20000,
                data: {
                    total: items.length,
                    items: items
                }
            }
        }
    }
]
