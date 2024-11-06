package main

import (
	"context"
	"log"
	"net"
	"thesis/rpc_go/pb"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

type server struct {
	pb.UnimplementedTestServiceServer
}

func (s *server) TestMethod(
	ctx context.Context, in *pb.TestRequest,
	)(
	*pb.TestResponse, error,
	){

		return &pb.TestResponse{
			Message: "Hello " + in.Name,
		}, nil

}


func main() {

	listener, err := net.Listen("tcp", ":8080")

	if err != nil {
		log.Fatalln("Failed to create listener: ", err)
	}

	s := grpc.NewServer()
	reflection.Register(s)

	pb.RegisterTestServiceServer(s, &server{})

	if err := s.Serve(listener); err != nil {
		log.Fatalln("Failed to serve: ", err)
	}
	
}
