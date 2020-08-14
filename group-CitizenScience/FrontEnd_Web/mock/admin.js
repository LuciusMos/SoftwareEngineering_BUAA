import Mock from 'mockjs'

const admin_data = Mock.mock({
    'items|10': [{
        id: '@id',
        name: '@sentence(2, 2)',
        display_time: '@datetime',
        address: '@sentence(3,10)'
    }]
})

export default [
    {
        url: '/vue-admin-template/menu1/admin/list',
        type: 'get',
        response: config => {
            const items = admin_data.items
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
