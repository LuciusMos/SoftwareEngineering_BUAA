import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '主页', icon: 'dashboard' }
    }]
  }
];

export const asyncRoutes = [
  {
    path: '/research_management',
    component: Layout,
    redirect: 'noRedirect',
    name: 'research_management',
    meta: { title: '项目管理', icon: 'example' },
    children: [
      {
        path: 'all_research',
        name: 'All_research',
        component: () => import('@/views/research_management/all_research/index'),
        meta: { title: '查看项目', icon: 'table', roles: ['admin'] }
      },
      {
        path: 'my_research',
        name: 'My_research',
        component: () => import('@/views/research_management/my_research/index'),
        meta: { title: '我的项目', icon: 'tree', roles:['scientist','assistant'] }
      },
      {
        path: 'review_research',
        name: 'Review_research',
        component: () => import('@/views/research_management/review_research/index'),
        meta: { title: '项目审核', icon: 'skill', roles: ['admin'] }
      }
    ]
  },

  {
    path: '/form',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Form',
        component: () => import('@/views/form/index'),
        meta: { title: '项目发布', icon: 'form', roles: ['scientist'] }
      }
    ]
  },

  {
    path: '/data',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Data',
        component: () => import('@/views/data/index'),
        meta: { title: '数据管理', icon: 'search', roles: ['scientist','assistant'] }
      }
    ]
  },

  // {
  //   path: '/Myvisual',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       name: 'Myvisual',
  //       component: () => import('@/views/visual/MyVisual'),
  //       meta: { title: '数据可视化', icon: 'chart', roles: ['scientist','assistant'] }
  //     }
  //   ]
  // },
  // {
  //   path: '/visual',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       name: 'visual',
  //       component: () => import('@/views/visual/Selection'),
  //       // meta: { title: '添加数据可视化', icon: 'search', roles: ['scientist','assistant'] }
  //       }
  //   ]
  // },
  {
    path: '/visualization',
    component: Layout,
    redirect: 'nodirect',
    name:'visualization',
    meta: { title: '数据可视化', icon: 'chart', roles: ['scientist', 'assistant'] },
    children: [
      {
        path: 'myvisual',
        name: 'Myvisual',
        component: () => import('@/views/visual/MyVisual'),
        meta: { title: '我的可视化', icon: 'example', roles: ['scientist','assistant'] }
      },
      {
        path: 'new_visual',
        name: 'New_Visual',
        component: () => import('@/views/visual/Selection'),
        meta: { title: '新建可视化', icon: 'edit', roles: ['scientist','assistant'] }
        }
    ]
  },

  {
    path: '/user_management',
    component: Layout,
    redirect: 'noRedirect',
    name: 'User_management',
    meta: {
      title: '用户管理',
      icon: 'nested',
      roles: ['admin','scientist']
    },
    children: [
      {
        path: 'all_user',
        name: 'All_user',
        redirect: 'noRedirect',
        component: () => import('@/views/user_management/all_user'),
        meta: { title: '查看用戶',icon:"peoples"},
        children: [
          // {
          //   path: 'admin',
          //   component: () => import('@/views/user_management/all_user/admin'),
          //   name: 'Admin',
          //   meta: { title: '管理员' ,icon:"user"}
          // },
          {
            path: 'scientist',
            component: () => import('@/views/user_management/all_user/scientist'),
            name: 'Scientist',
            meta: { title: '科学家' ,icon:"user"}
          },
          {
            path: 'assistant',
            component: () => import('@/views/user_management/all_user/assistant'),
            name: 'Assistant',
            meta: { title: '助理' ,icon:"user"}
          },
          {
            path: 'volunteer',
            component: () => import('@/views/user_management/all_user/volunteer'),
            name: 'Volunteer',
            meta: { title: '志愿者' ,icon:"user"}
          }
        ]
      },
      {
        path: 'my_team',
        component: () => import('@/views/user_management/my_team/index'),
        meta: { title: '我的团队', roles: ['scientist','assistant'] ,icon:"education"}
      },
      {
        path: 'apply_assistant',
        component: () => import('@/views/user_management/apply_assistant/index'),
        meta: { title: '审核助理', roles: ['scientist'] ,icon:"documentation"}
      },
      {
        path: 'authentication_scientist',
        component: () => import('@/views/user_management/authentication_scientist/index'),
        meta: { title: '科学家认证', roles: ['admin'],icon:"education" }
      }
    ]
  },

  {
    path: '/aboutUs',
    component: Layout,
    children: [
      {
        path: '',
        name: 'About_us',
        component: () => import('@/views/aboutUs'),
        meta: { title: '关于我们', icon: 'link' }
      }
    ]
  },
  {
    path: '/feedback_admin',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Feedback_admin',
        component: () => import('@/views/feedback_admin'),
        meta: { title: '用户反馈', icon: 'email', roles: ['admin'] }
        }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
