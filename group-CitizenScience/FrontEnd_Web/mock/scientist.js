import Mock from 'mockjs'

const scientist_data = Mock.mock({
    'items|10': [{
        id: '@id',
        name: '@sentence(2, 3)',
        display_time: '@datetime',
        address: '@sentence(10,20)'
    }]
})

export default [
    {
        url: '/vue-admin-template/menu1/scientist/list',
        type: 'get',
        response: config => {
            const items = scientist_data.items
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
