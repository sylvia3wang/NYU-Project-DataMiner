/**
 * Created by xtzhao on 2018/12/12.
 */
$(document).ready(function () {
    $('#table_transactions').DataTable();

    // 路径配置
    require.config({
        paths: {
            echarts: 'http://echarts.baidu.com/build/dist'
        }
    });
    // 使用
    require(
        [
            'echarts',
            'echarts/chart/line', // 使用柱状图就加载bar模块，按需加载
            'echarts/chart/pie' // 使用柱状图就加载bar模块，按需加载
        ],
        function (ec) {
            $.ajax({
                type: "get",
                dataType: "html",
                url: '/api/btc_price',
                success: function (data) {
                    if (data != "") {
                        data = $.parseJSON(data);

                        if (data['status'] == 0){
                            // 基于准备好的dom，初始化echarts图表
                            var myChart = ec.init(document.getElementById('btc_price_div'));

                            var option = {
                                title : {
                                    text: 'BTC-Prices',
                                },
                                tooltip : {
                                    trigger: 'axis'
                                },
                                legend: {
                                    data:['BTC-Prices']
                                },
                                toolbox: {
                                    show : true,
                                    feature : {
                                        mark : {show: true},
                                        dataView : {show: true, readOnly: false},
                                        magicType : {show: true, type: ['line', 'bar']},
                                        restore : {show: true},
                                        saveAsImage : {show: true}
                                    }
                                },
                                calculable : true,
                                xAxis : [
                                    {
                                        type : 'category',
                                        boundaryGap : false,
                                        data : data['times'],
                                        axisLabel : {
                                            rotate:15
                                        }
                                    }
                                ],
                                yAxis : [
                                    {
                                        type : 'value',
                                        axisLabel : {
                                            formatter: '{value} $',

                                        }
                                    }
                                ],
                                series : [
                                    {
                                        type:'line',
                                        data:data['prices'],
                                        markPoint : {
                                            data : [
                                                {type : 'max', name: '最大值'},
                                                {type : 'min', name: '最小值'}
                                            ]
                                        },
                                        markLine : {
                                            data : [
                                                {type : 'average', name: '平均值'}
                                            ]
                                        }
                                    }
                                ]
                            };


                            // 为echarts对象加载数据
                            myChart.setOption(option);
                        }else{
                            alert(data['message']);
                        }
                    }
                }
            });

            $.ajax({
                type: "get",
                dataType: "html",
                url: '/api/cash_btc',
                success: function (data) {
                    if (data != "") {
                        data = $.parseJSON(data);

                        if (data['status'] == 0){
                            // 基于准备好的dom，初始化echarts图表
                            var myChart = ec.init(document.getElementById('ratio_div'));

                            var option = {
                                title : {
                                    text: 'Cash/BTC',
                                    x:'center'
                                },
                                tooltip : {
                                    trigger: 'item',
                                    formatter: "{b} : {c} ({d}%)"
                                },
                                legend: {
                                    orient : 'vertical',
                                    x : 'left',
                                    data:['Cash','BTC']
                                },
                                toolbox: {
                                    show : true,
                                    feature : {
                                        mark : {show: true},
                                        dataView : {show: true, readOnly: false},
                                        magicType : {
                                            show: true,
                                            type: ['pie', 'funnel'],
                                            option: {
                                                funnel: {
                                                    x: '25%',
                                                    width: '50%',
                                                    funnelAlign: 'left',
                                                    max: 1548
                                                }
                                            }
                                        },
                                        restore : {show: true},
                                        saveAsImage : {show: true}
                                    }
                                },
                                calculable : true,
                                series : [
                                    {
                                        type:'pie',
                                        radius : '55%',
                                        center: ['50%', '60%'],
                                        data:[
                                            {value:data['cash'], name:'Cash'},
                                            {value:data['btc'], name:'BTC'}
                                        ]
                                    }
                                ]
                            };

                            // 为echarts对象加载数据
                            myChart.setOption(option);
                        }else{
                            alert(data['message']);
                        }
                    }
                }
            });

            $.ajax({
                type: "get",
                dataType: "html",
                url: '/api/upls',
                success: function (data) {
                    if (data != "") {
                        data = $.parseJSON(data);

                        if (data['status'] == 0){
                            // 基于准备好的dom，初始化echarts图表
                            var myChart = ec.init(document.getElementById('upl_div'));

                            var option = {
                                title : {
                                    text: 'UPL',
                                },
                                tooltip : {
                                    trigger: 'axis'
                                },
                                legend: {
                                    data:['UPL']
                                },
                                toolbox: {
                                    show : true,
                                    feature : {
                                        mark : {show: true},
                                        dataView : {show: true, readOnly: false},
                                        magicType : {show: true, type: ['line', 'bar']},
                                        restore : {show: true},
                                        saveAsImage : {show: true}
                                    }
                                },
                                calculable : true,
                                xAxis : [
                                    {
                                        type : 'category',
                                        boundaryGap : false,
                                        data : data['times'],
                                        axisLabel : {
                                            rotate:15
                                        }
                                    }
                                ],
                                yAxis : [
                                    {
                                        type : 'value',
                                        axisLabel : {
                                            formatter: '{value} $',

                                        }
                                    }
                                ],
                                series : [
                                    {
                                        type:'line',
                                        data:data['upls'],
                                        markPoint : {
                                            data : [
                                                {type : 'max', name: '最大值'},
                                                {type : 'min', name: '最小值'}
                                            ]
                                        },
                                        markLine : {
                                            data : [
                                                {type : 'average', name: '平均值'}
                                            ]
                                        }
                                    }
                                ]
                            };


                            // 为echarts对象加载数据
                            myChart.setOption(option);
                        }else{
                            alert(data['message']);
                        }
                    }
                }
            });
        }
    );



    // $.ajax({
    //     type: "get",
    //     url: '/api/upls',
    //     success: function (data) {
    //         if (data != "") {
    //             data = $.parseJSON(data);
    //
    //             if (data['status'] == 0){
    //
    //                 // 基于准备好的dom，初始化echarts图表
    //                 var myChart_1 = ec.init(document.getElementById('upl_div'));
    //
    //                 var option_1 = {
    //                     title : {
    //                         text: 'UPL',
    //                     },
    //                     tooltip : {
    //                         trigger: 'axis'
    //                     },
    //                     legend: {
    //                         data:['UPL']
    //                     },
    //                     toolbox: {
    //                         show : true,
    //                         feature : {
    //                             mark : {show: true},
    //                             dataView : {show: true, readOnly: false},
    //                             magicType : {show: true, type: ['line', 'bar']},
    //                             restore : {show: true},
    //                             saveAsImage : {show: true}
    //                         }
    //                     },
    //                     calculable : true,
    //                     xAxis : [
    //                         {
    //                             type : 'category',
    //                             boundaryGap : false,
    //                             data : data['times'],
    //                             axisLabel : {
    //                                 rotate:40
    //                             }
    //                         }
    //                     ],
    //                     yAxis : [
    //                         {
    //                             type : 'value',
    //                             axisLabel : {
    //                                 formatter: '{value} $',
    //
    //                             }
    //                         }
    //                     ],
    //                     series : [
    //                         {
    //                             type:'line',
    //                             data:data['prices'],
    //                             markPoint : {
    //                                 data : [
    //                                     {type : 'max', name: '最大值'},
    //                                     {type : 'min', name: '最小值'}
    //                                 ]
    //                             },
    //                             markLine : {
    //                                 data : [
    //                                     {type : 'average', name: '平均值'}
    //                                 ]
    //                             }
    //                         }
    //                     ]
    //                 };
    //
    //
    //                 // 为echarts对象加载数据
    //                 myChart_1.setOption(option_1);
    //
    //                 // 使用
    //                 // require(
    //                 //     [
    //                 //         'echarts',
    //                 //         'echarts/chart/line' // 使用柱状图就加载bar模块，按需加载
    //                 //     ],
    //                 //     function (ec) {
    //                 //
    //                 //     }
    //                 // );
    //             }else{
    //                 alert(data['message']);
    //             }
    //         }
    //     }
    // });
})


