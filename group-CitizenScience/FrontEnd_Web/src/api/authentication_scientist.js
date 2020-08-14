import request from '@/utils/request'

export function getSciAuthenticationList(params) {
  return request({
    url: '/vue-admin-template/authentication_scientist/list',
    method: 'get',
    params
  })
}
