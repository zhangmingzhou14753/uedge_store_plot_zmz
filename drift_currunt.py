
def current():

    ixp1_indices = bbb.ixp1[com.ixpt1, 1:com.iysptrx+1]  # 获取所有 i
    index_range = np.arange(1, com.iysptrx+1)  # 生成 [1, 2, ..., com.iysptrx]

    total_sum = np.sum(
        bbb.v2ce[com.ixpt1, index_range, 0] *
        com.sx[com.ixpt1, index_range] *
        bbb.ni[ixp1_indices, index_range, 0] *  # 用 ixp1_indices 作为索引
        bbb.rbfbt[com.ixpt1, index_range]
    )

    print('EXB radial contribute in Private regions:' ,total_sum)

    ixp1_indices = bbb.ixp1[0:com.ixpt1[0],com.iysptrx+1]
    index_range = np.arange(1,com.ixpt1[0]+1)-1  # index_range = np.arange(0:com.ixpt1[0])
    total_sum = np.sum(bbb.vyce[index_range,com.iysptrx+1,0]*com.sy[index_range,com.iysptrx+1]*bbb.ni[ixp1_indices,com.iysptrx+1,0])
    print('EXB poloidal  contribute in Inner leg:' ,total_sum)

    ixp1_indices = bbb.ixp1[com.ixpt2[0]+1:com.nx+1,com.iysptrx+1]
    index_range = np.arange(com.ixpt2[0]+1,com.nx+1)
    total_sum = np.sum(bbb.vyce[index_range,com.iysptrx+1,0]*com.sy[index_range,com.iysptrx+1]*bbb.ni[ixp1_indices,com.iysptrx+1,0])
    print('EXB poloidal  contribute in Outer leg:' ,total_sum)

    ixp1_indices = bbb.ixp1[com.ixpt1,com.iysptrx+1:-1]
    index_range = np.arange(com.iysptrx+1,com.ny+1) 
    total_sum = np.sum(bbb.v2ce[com.ixpt1,index_range,0]*com.sx[com.ixpt1,index_range]*bbb.ni[ixp1_indices,index_range,0]
                *bbb.rbfbt[com.ixpt1,index_range])

    print('EXB poloidal  contribute in Inner divertor:' ,total_sum)


    ixp1_indices = bbb.ixp1[com.ixpt2,com.iysptrx+1:-1]
    index_range = np.arange(com.iysptrx+1,com.ny+1)
    total_sum = np.sum(bbb.v2ce[com.ixpt2,index_range,0]*com.sx[com.ixpt2,index_range]*bbb.ni[ixp1_indices,index_range,0]
                *bbb.rbfbt[com.ixpt2,index_range])

    print('EXB poloidal  contribute in Outer divertor:' ,total_sum)




