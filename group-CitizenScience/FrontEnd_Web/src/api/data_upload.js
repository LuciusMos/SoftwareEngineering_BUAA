import request from '@/utils/request'

export function getDataUpload(params) {
  return request({
    url: '/vue-admin-template/data_upload/list',
    method: 'get',
    params
  })
}
