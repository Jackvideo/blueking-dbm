package handler_rpc

import (
	"dbm-services/mysql/db-remote-service/pkg/config"
	"fmt"
	"log/slog"
	"net/http"
	"strings"

	"dbm-services/mysql/db-remote-service/pkg/rpc_core"

	"github.com/gin-gonic/gin"
)

func generalHandler(rpcEmbed rpc_core.RPCEmbedInterface) func(*gin.Context) {
	return func(c *gin.Context) {
		req := queryRequest{
			ConnectTimeout: 2,
			QueryTimeout:   600, // 默认超时时间 10 分钟
			Force:          false,
			Timezone:       config.RuntimeConfig.Timezone,
		}

		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(
				http.StatusBadRequest, gin.H{
					"code": 1,
					"data": "",
					"msg":  err.Error(),
				},
			)
			return
		}
		req.TrimSpace()

		slog.Info(
			"enter rpc handler",
			slog.String("addresses", strings.Join(req.Addresses, ",")),
			slog.String("cmds", strings.Join(req.Cmds, ",")),
			slog.Bool("force", req.Force),
			slog.Int("connect_timeout", req.ConnectTimeout),
			slog.Int("query_timeout", req.QueryTimeout),
		)
		dupAddrs := findDuplicateAddresses(req.Addresses)
		slog.Info("duplicate address", slog.String("addresses", strings.Join(dupAddrs, ",")))

		if len(dupAddrs) > 0 {
			c.JSON(
				http.StatusBadRequest, gin.H{
					"code": 1,
					"data": "",
					"msg":  fmt.Sprintf("duplicate addresses %s", dupAddrs),
				},
			)
		}

		rpcWrapper := rpc_core.NewRPCWrapper(
			req.Addresses, req.Cmds,
			rpcEmbed.User(), rpcEmbed.Password(),
			req.ConnectTimeout, req.QueryTimeout, req.Timezone, req.Force,
			rpcEmbed,
		)

		resp := rpcWrapper.Run()

		c.JSON(
			http.StatusOK, gin.H{
				"code": 0,
				"data": resp,
				"msg":  "",
			},
		)
	}
}
