import request from '@/utils/request'

export function getAdminList(params) {
  return request({
    url: '/vue-admin-template/menu1/admin/list',
    method: 'get',
    params
  })
}
