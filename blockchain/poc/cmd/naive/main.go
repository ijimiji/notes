package main

import (
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"time"
)

type InBlock struct {
	Index     int   `json:"index"`
	Timestamp int64 `json:"timestamp"`
	Data      []any `json:"data"`
}

func (b *Block) CalculateHash() string {
	data, _ := json.Marshal(b.InBlock)
	raw := md5.Sum(data)

	hash := hex.EncodeToString(raw[:])
	return hash
}

type Block struct {
	InBlock
	PrevHash string
	Hash     string
}

func NewBlock() *Block {
	block := &Block{
		InBlock: InBlock{
			Timestamp: time.Now().Unix(),
		},
	}
	block.Hash = block.CalculateHash()

	return block
}

type Blockchain struct {
	Blocks []*Block
}

func (o *Blockchain) GetLastBlock() *Block {
	return o.Blocks[len(o.Blocks)-1]
}

func (o *Blockchain) AddBlock(block *Block) {
	block.PrevHash = o.GetLastBlock().Hash
	o.Blocks = append(o.Blocks, block)
}

func NewBlockchain() *Blockchain {
	return &Blockchain{
		Blocks: []*Block{NewBlock()},
	}
}

func (o *Blockchain) IsValid() bool {
	for i := 1; i < len(o.Blocks); i++ {
		current := o.Blocks[i]
		prev := o.Blocks[i-1]

		if current.PrevHash != prev.Hash || current.Hash != current.CalculateHash() {
			fmt.Printf("%v %s\n", current, current.CalculateHash())
			return false
		}
	}
	return true
}

func main() {
	blockchain := NewBlockchain()
	blockchain.AddBlock(NewBlock())
	blockchain.AddBlock(NewBlock())

	fmt.Println(blockchain.IsValid())
}
