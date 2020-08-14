import Mock from 'mockjs'

const assistant_data = Mock.mock({
    'items|10': [{
        id: '@id',
        name: '@sentence(2, 3)',
        scientist: '@sentence(2, 3)',
        display_time: '@datetime',
        address: '@sentence(10,20)'
    }]
})

export default [
    {
        url: '/vue-admin-template/menu1/assistant/list',
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
